#!/usr/bin/env python3
"""Keep `last_edited` current on posts that are already published.

Runs as a pre-commit hook. When a commit changes what a published post shows (its
title, description, text, or a file under assets/ that it uses), this sets
`last_edited` to today and fails the commit, so the post can be staged again.
Drafts, new posts and posts still dated in the future are left alone.
"""

import datetime as dt
import pathlib
import re
import subprocess
import sys


def git(*args):
    done = subprocess.run(["git", *args], capture_output=True, check=True)
    return done.stdout.decode("utf-8", "replace")


def split(text):
    """Return (front matter, body); front matter is empty if there is none."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4 : end + 1], text[end + 5 :]
    return "", text


def field(front, name):
    match = re.search(rf"^{name}:[ \t]*(.*)$", front, re.MULTILINE)
    return match.group(1).strip().strip("\"'") if match else ""


def visible(text):
    """The parts of a post a reader sees. Tags, series and the like don't count."""
    front, body = split(text)
    return field(front, "title"), field(front, "description"), body.strip()


def published_at(front, path):
    raw = field(front, "date")
    for pattern in ("%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            when = dt.datetime.strptime(raw, pattern)
            break
        except ValueError:
            continue
    else:
        when = dt.datetime.strptime(pathlib.Path(path).name[:10], "%Y-%m-%d")
    return when if when.tzinfo else when.astimezone()


def stamp(text, today):
    front, body = split(text)
    line = f"last_edited: {today}\n"
    if re.search(r"^last_edited:.*\n", front, re.MULTILINE):
        front = re.sub(r"^last_edited:.*\n", line, front, flags=re.MULTILINE)
    elif re.search(r"^date:.*\n", front, re.MULTILINE):
        front = re.sub(
            r"^(date:.*\n)", rf"\g<1>{line}", front, count=1, flags=re.MULTILINE
        )
    else:
        front += line
    return f"---\n{front}---\n{body}"


def main():
    try:
        git("rev-parse", "--verify", "HEAD")
    except subprocess.CalledProcessError:
        return 0  # first commit: nothing has been published yet

    now = dt.datetime.now().astimezone()
    today = now.date().isoformat()
    changes = [
        line.split("\t")
        for line in git("diff", "--cached", "--name-status", "-M").splitlines()
    ]
    assets = {path for change in changes for path in change[1:] if path.startswith("assets/")}
    renamed_from = {c[2]: c[1] for c in changes if c[0].startswith("R")}
    committed = set(git("ls-tree", "-r", "--name-only", "HEAD", "_posts").splitlines())

    stamped = []
    for path in git("ls-files", "_posts").splitlines():
        before = renamed_from.get(path, path)
        if before not in committed:
            continue  # a new post
        old = git("show", f"HEAD:{before}")
        if published_at(split(old)[0], before) > now:
            continue  # not out yet
        new = git("show", f":{path}")
        changed = visible(old) != visible(new) or any(f"/{a}" in new for a in assets)
        if not changed or field(split(new)[0], "last_edited") == today:
            continue
        file = pathlib.Path(path)
        file.write_text(stamp(file.read_text(encoding="utf-8"), today), encoding="utf-8")
        stamped.append(path)

    for path in stamped:
        print(f"set last_edited to {today} in {path}; stage it and commit again")
    return 1 if stamped else 0


if __name__ == "__main__":
    sys.exit(main())
