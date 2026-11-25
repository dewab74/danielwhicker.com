---
layout: post
date: 2026-10-13 09:00:00 -0500
title: "mping: ping a pile of hosts from one terminal screen"
description: "A terminal UI that probes a list of hosts over ICMP, TCP, HTTP or HTTPS and shows what's up, how fast, and how often it fails."
accent: infrastructure
tags: [cli, networking, monitoring]
---

I'm frequently doing VM migrations, host migrations, or other work where I want an
ad-hoc, at-a-glance report on whether what I'm migrating is done, up or down. Or
whether I need to dust off [my resume](https://bifrost.cc/resume.html).

So I wrote mping, a terminal UI for watching a bunch of hosts at once. A TUI,
because given the choice between a GUI and a TUI, I'll take the TUI. Give it a
list and it probes all of them concurrently, then shows each one's status,
round-trip time, success and failure counts, when it last answered, and the last
error.

It isn't limited to ping. Each host can be probed over ICMP, TCP, HTTP or HTTPS, so
the same screen can tell you a router answers, a port is open, and a web page
returns a 200.

{% include get-it.html id="mping" %}

<figure>
<img src="{{ '/assets/img/mping/demo.gif' | relative_url }}"
  width="1011" height="567"
  alt="A terminal recording of mping. Six hosts show their status and round-trip times, with one
  red row. A dialog opens and two more hosts are typed in, the list grows to eight, and the
  settings dialog opens.">
<figcaption>A quick tour: adding hosts, then the settings. The red row is 192.0.2.1, a reserved
documentation address, so it's always down. You can also
<a href="{{ '/assets/casts/mping-demo.cast' | relative_url }}">download the recording</a> and play it
with <code>asciinema play</code>.</figcaption>
</figure>

## Using it

```bash
mping example.com 1.1.1.1
mping example.com tcp:api.example.com:8443 icmp:gateway.example.com
mping https://example.com/health
mping -f hosts.txt
```

Put one host per line in a file, or list them as arguments. Any entry can override
the protocol, like `tcp:host:8443`, or be a URL for an HTTP check.

Targets aren't fixed, either. While it's running, `a` adds hosts and `d` deletes the
selected one, and `s` opens the settings (protocol, interval, timeout, sort order,
theme). `o` cycles the sort and `q` quits.

<figure>
<img src="{{ '/assets/img/mping/main.png' | relative_url }}"
  width="1146" height="643"
  alt="mping's main screen: a table of hosts with mode, address, round-trip time, status,
  success and failure counts. Six rows are green and one is red.">
<figcaption>The main screen. Six hosts answer, and the one that doesn't is red.</figcaption>
</figure>

<figure>
<img src="{{ '/assets/img/mping/settings.png' | relative_url }}"
  width="1146" height="643"
  alt="mping's settings dialog over the host table, with ping, sort and display sections: protocol,
  TCP port, ICMP backend, interval, timeout, system args, sort key and direction, theme and
  refresh.">
<figcaption>The settings dialog, opened with <code>s</code>.</figcaption>
</figure>

## Themes

It ships with nine themes: default, Dracula, Nord, Solarized dark and light, and the
four Catppuccin flavors. A theme is a small text file of colors, or you can define
one inline in the YAML config. `mping --list-themes` shows what it found.

<div class="figure-row">
<figure class="figure-medium">
<img src="{{ '/assets/img/mping/mocha.png' | relative_url }}"
  width="1146" height="643"
  alt="mping in the Catppuccin Mocha theme: soft pastel colors on a dark background.">
<figcaption>Catppuccin Mocha</figcaption>
</figure>
<figure class="figure-medium">
<img src="{{ '/assets/img/mping/nord.png' | relative_url }}"
  width="1146" height="643"
  alt="mping in the Nord theme: muted blue-gray colors on a dark background.">
<figcaption>Nord</figcaption>
</figure>
</div>

## Getting it

Homebrew is the easy way. It builds from source, so it needs Go, which Homebrew
will pull in:

```bash
brew tap dewab-org/custom && { brew trust --formula dewab-org/custom/mping 2>/dev/null || true; } && brew install dewab-org/custom/mping
```

Or take a tarball from the release page: Linux on amd64 or arm64, and macOS on Apple
silicon. The binaries are statically linked.

## Where it stands

The latest release is v0.2.0, from August. There's no Intel Mac build, and nothing
for Windows.

There's also a SwiftUI desktop client, [mping-mac](https://github.com/dewab-org/mping-mac),
in its own repo. It's new, and it has no release yet.
