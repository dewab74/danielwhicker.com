---
layout: post
date: 2026-12-08 09:00:00 -0600
title: "Uptime Kuma, on the Mac desktop where I can actually see it"
description: "A small macOS widget that shows what's down in Uptime Kuma, parked at the edge of a screen instead of in a browser tab."
accent: infrastructure
tags: [macOS, homelab, monitoring]
---

I run [Uptime Kuma](https://github.com/louislam/uptime-kuma) at home, and my
instance is ridiculous. It's watching 101 monitors. A house does not need 101
monitors. I have them anyway.

I wanted to see what's down without opening a web page. Specifically, a desktop
widget I could park at the bottom of my second screen and glance at.

The dashboard is slow to render, because I'd been too lazy to build a status page
and so it draws everything, and there's a lot of everything. I also don't want
another browser tab for something I only glance at.

I couldn't find a native macOS desktop widget for Kuma. There are menu bar apps, an
xbar plugin, and iPhone widgets you can drag onto a Mac desktop, but those are
built for the phone, and the phone has to be nearby. So I wrote one.

{% include get-it.html id="kuma-status" %}

## What it shows

The small widget gives you the overall verdict and the names of whatever is down.
The medium one adds the counts and the worst monitors with their recent
heartbeats. The large one groups the monitors like your status page does, with
heartbeat bars, 24-hour uptime and any pinned incident or maintenance.

<div class="figure-row">
<figure class="figure-small">
<img src="{{ '/assets/img/uptime-kuma/widget-small-light.png' | relative_url }}"
  width="420" height="420"
  alt="Small widget in light mode: one monitor is down, with its name under the verdict.">
</figure>
<figure class="figure-medium">
<img src="{{ '/assets/img/uptime-kuma/widget-medium-dark.png' | relative_url }}"
  width="808" height="420"
  alt="Medium widget in dark mode: the failing monitor first, then three healthy ones.">
</figure>
</div>
<figure class="figure-narrow">
<img src="{{ '/assets/img/uptime-kuma/widget-large-light.png' | relative_url }}"
  width="808" height="844"
  alt="Large widget in light mode: monitors grouped under Network and Apps, with
  heartbeat bars and 24-hour uptime, and the one failing monitor in red.">
<figcaption>The three sizes, showing sample data.</figcaption>
</figure>

A menu bar icon shows the overall state and a count of what's broken. Broken things
sort to the top. If the data goes stale or a check fails, the widget dims and says
it's offline, so a dead server doesn't look healthy.

## You still need a status page

It reads the same public endpoints the web page does, so there's no password or
API key on the Mac. The catch is that only monitors on a published status page show
up. One you never share works fine as a private dashboard.

Setup: paste your Kuma address (or a status page link), hit Test, and add the
widget from Edit Widgets. Plain `http://` works on a LAN, and there's a switch for
self-signed certificates.

## Why there's a menu bar app too

macOS widgets don't get a timer. The system refreshes them every fifteen minutes or
so, which is too slow for this. So the menu bar app polls every 60 seconds and only
tells the widget to redraw when something actually changes. Without the app, the
widget fetches on its own, just more slowly.

I haven't checked how that holds up over several days of sleep and wake. That's on
my list.

## Where it stands

It's v0.1.0, so treat it that way.

- Tested against a real Uptime Kuma 2.5.3 on macOS 27. Kuma 1.23 only against a
  mock of its API.
- Needs macOS 14 or later.
- Signed with a development certificate but not notarized, so the first launch
  needs **System Settings, Privacy & Security, Open Anyway**. Releases ship with a
  SHA-256.
- One status page per widget, and no notifications. Kuma does those fine already.

I haven't decided what to do with it beyond this. It might go in the App Store, it
might become a Homebrew Cask, or it might just stay here for me and whoever
happens to stumble across it. For now it's a zip on the releases page.

Kuma Status isn't affiliated with or endorsed by the Uptime Kuma project.
