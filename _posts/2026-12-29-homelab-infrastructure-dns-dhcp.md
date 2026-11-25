---
layout: post
date: 2026-12-29 09:00:00 -0600
title: "Homelab: DNS, DHCP and the plumbing"
description: "The firewall, name resolution, addresses, certificates and a few Raspberry Pis."
accent: infrastructure
tags: [homelab, dns, dhcp, opnsense]
series: homelab
series_part: 4
---

## The bouncer

OPNsense routes between the networks and keeps home, lab, IoT and guest traffic apart,
so the smart home gear sits at its own table. Its rules, blocklists and intrusion
detection settings are code, and AWX runs the Ansible playbooks for them every night.

## It's always DNS

Two hosts, dns01 and dns02, run both in containers.

<figure>
<picture>
<source media="(prefers-color-scheme: dark)"
  srcset="{{ '/assets/img/homelab/dns-dark.svg' | relative_url }}">
<img src="{{ '/assets/img/homelab/dns-light.svg' | relative_url }}"
  width="591" height="516" loading="lazy"
  alt="A diagram of DNS and DHCP. The home network gets names and addresses from two
  container hosts, dns01 and dns02. Each runs Technitium, Kea with a Stork agent, and
  PostgreSQL with Patroni. A Raspberry Pi witness, dns0q, breaks ties, and a Stork server
  in k3s manages DHCP.">
</picture>
<figcaption>Two of nearly everything, plus a tie-breaker.</figcaption>
</figure>

- **DNS.** Technitium, with DNS01 as the primary and DNS02 as the secondary.
- **DHCP.** Kea on DHCP01 and DHCP02, as a high availability pair. Its database is
  PostgreSQL under Patroni, with a Raspberry Pi to break ties. Small box, big vote.
- **Registration.** Kea adds clients to Technitium with dynamic DNS.
- **Management.** A Stork agent sits next to each Kea. The Stork server runs in
  k3s.

### Pi-hole perks, no Pi-hole

I'm also using public block lists with Technitium, so I get a lot of the "Pi-hole"
benefits without the "Pi-hole" limitations.

What I get:

- Blocking and a full DNS server in one, with my own primary and secondary zones, zone
  transfers and DNSSEC.
- Both servers managed as a cluster from one console.
- Encrypted DNS built in. Pi-hole's guide for that adds a separate program.

What to watch for:

- Different rules for different clients need an extra Technitium app. Pi-hole has
  groups built in.
- It's still DNS blocking. It can't touch an ad served from the same name as the
  content, and a device that brings its own encrypted DNS walks right past it unless
  the firewall objects.

## Papers, please

- **Certificates.** Everything has a real, signed one: step-ca internally, Let's
  Encrypt externally. Almost all of them are short-lived.
- **The rest.** A directory, a secrets manager, and single sign-on with passkeys.

## The little guys

- **dns0q** is the tie-breaker for the DHCP database.
- **rpi-usbip** is the print and scan server. CUPS shares the Dell laser printer with
  AirPrint, and AirSane shares the USB scanner.
- **Batocera** runs arcade and retro games. Critical infrastructure.
