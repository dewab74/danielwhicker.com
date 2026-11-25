---
layout: post
date: 2027-01-05 09:00:00 -0600
title: "Homelab: getting in from outside"
description: "A DMZ with paired reverse proxies and SSH bastions, plus Tailscale."
accent: infrastructure
tags: [homelab, networking, security]
series: homelab
series_part: 5
---

## The front porch

Services published from home go through a DMZ, and the firewall filters what passes
between it and the inside.

<figure>
<picture>
<source media="(prefers-color-scheme: dark)"
  srcset="{{ '/assets/img/homelab/edge-dark.svg' | relative_url }}">
<img src="{{ '/assets/img/homelab/edge-light.svg' | relative_url }}"
  width="539" height="518" loading="lazy"
  alt="A diagram of outside access. Traffic from the internet passes the OPNsense
  firewall. Published services go to a DMZ VLAN holding two edge proxies and two SSH
  bastions, separate from the inside networks.">
</picture>
<figcaption>The way in. Please wipe your feet.</figcaption>
</figure>

- **Edge proxies.** edge-proxy-1 and edge-proxy-2, a redundant pair of reverse
  proxies.
- **Bastions.** bastion-1 and bastion-2, a redundant pair of SSH jump hosts.

## The side door

I use Tailscale for remote access into my network. I tried Funnel, but it was too
bandwidth constrained. I used to have AWS VPS instances where I could have tried
Headscale, but I didn't want to keep paying for resources I could otherwise get for
free.
