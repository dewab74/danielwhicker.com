# danielwhicker.com

Source for [danielwhicker.com](https://danielwhicker.com), a small static blog
about the projects I build and what they're good for.

It is plain Jekyll with no plugins and no JavaScript beyond an optional
click-to-load comment widget, so GitHub Pages can build it as is.

## Status

Early. Owned and maintained by Daniel Whicker.

## Requirements

- Ruby and Jekyll 3.9 or newer to preview locally (`gem install jekyll`).
- [pre-commit](https://pre-commit.com/) for the commit hooks.

## Usage

Preview the site, including unpublished drafts:

```bash
jekyll serve --drafts
```

Then open <http://127.0.0.1:4000>.

### Writing a post

1. Create `_drafts/some-slug.md` with front matter (`layout: post`, `title`,
   `description`, `tags`).
2. Review it locally with `jekyll serve --drafts`.
3. To publish, move it to `_posts/YYYY-MM-DD-some-slug.md` and push.

A post dated in the future stays off the site until its date. A daily workflow
(`.github/workflows/scheduled-publish.yml`) asks GitHub Pages to rebuild, which
is what makes it appear. The source is visible in the repo before then.

`_drafts/` is git-ignored on purpose, so an unreviewed draft cannot reach the
remote by accident.

## Configuration

Site settings live in `_config.yml`. Comments are off until the `comments`
block there is filled in (see the comments in that file). A post can opt out
with `comments: false`.

## Development setup

Clone, then **install the git hooks**:

```bash
pre-commit install
pre-commit run --all-files   # first run, to see where things stand
```

Git hooks live in `.git/hooks/`, which is not part of a clone, so this step is
per-machine and per-clone. Skipping it means your commits get no linting and
no credential-leak scanning.

Linting and secret scanning run at commit time rather than in CI, so failures
surface before a bad commit exists rather than after it has been pushed.

## Licenses and credits

Post text and images are copyright Daniel Whicker. The header artwork is also
Daniel Whicker's, all rights reserved.

The visual theme is Twilight Horizon, vendored under `assets/theme/` (MIT; see
`assets/theme/LICENSE`). It bundles Inter and JetBrains Mono (SIL Open Font
License 1.1) and uses Lucide icons (ISC). Each licence sits next to its files.
