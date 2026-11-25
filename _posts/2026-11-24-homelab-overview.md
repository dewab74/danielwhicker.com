---
layout: post
date: 2026-11-24 12:00:00 -0600
title: "My homelab runs a lot more than a house needs"
description: "What it's for, how it got here, and the rules I try to hold it to."
accent: infrastructure
tags: [homelab, hardware, networking]
series: homelab
series_part: 1
---

I run a lot more at home than a house needs. Yes, my homelab is overbuilt,
over-redundant and a bit ridiculous. You've been warned.

## Why on earth?

- **Learning.**
- **Prototyping things for work.** I frequently need short-lived lab environments,
  and I want them to come up from templates that already match how I do things. I
  use them to test Red Hat Satellite, Ansible Automation Platform, Docker,
  Kubernetes and Windows Active Directory in sandboxes, where breaking things is
  allowed.
- **Running the home network.** Name resolution, addresses, sign-on, monitoring and
  Home Assistant. You know, the stuff that has to keep working.

## Once upon a time

It started out running ESXi and vCenter, and today it runs Proxmox.

## Small boxes, on my desk

One of my guiding principles for picking hardware was to cut power consumption, and
with it noise and heat, because all of the equipment sits on my desk in my home
office. I haven't evolved my homelab into a pseudo-datacenter, or custom 3D printed
everything into a 10-inch rack as some folks have (yet!).

Another: buy small units so I can scale horizontally instead of making crazy big box
purchases. I don't have a YouTube channel feeding me money to buy a bunch of
enterprise equipment. And I really don't want to run this on old SPARC equipment
that "fell off the truck", for a multitude of reasons.

<figure>
<picture>
<source media="(prefers-color-scheme: dark)"
  srcset="{{ '/assets/img/homelab/hardware-dark.svg' | relative_url }}">
<img src="{{ '/assets/img/homelab/hardware-light.svg' | relative_url }}"
  width="720" height="593" loading="lazy"
  alt="A stacked hardware diagram. Machines sit on top in groups: a Proxmox cluster of
  three mini PCs, pve01 to pve03; two mini PCs, dns01 and dns02, for DNS and DHCP; and
  docker01 plus a Terramaster NAS for storage and containers. Below are three Raspberry
  Pis, dns0q, rpi-usbip and Batocera, with a laser printer and a scanner on USB hanging
  off rpi-usbip, and three wireless access points. Underneath everything are layers for a
  28-port managed switch, the OPNsense firewall and the internet.">
</picture>
<figcaption>The physical side, also known as my desk.</figcaption>
</figure>

## How it fits together

It's a mix. Some things run in containers on plain hosts, some in virtual machines
on Proxmox, and most applications on k3s, which itself runs in VMs. Yes, that's
containers inside virtual machines, next to containers on plain hosts. It's fine.

<figure>
<picture>
<source media="(prefers-color-scheme: dark)"
  srcset="{{ '/assets/img/homelab/services-dark.svg' | relative_url }}">
<img src="{{ '/assets/img/homelab/services-light.svg' | relative_url }}"
  width="720" height="743" loading="lazy"
  alt="A stacked network diagram. At the top are the internet and then the OPNsense
  firewall. Below it are a DMZ VLAN with two edge proxies and two SSH bastions, an IoT
  VLAN for smart home gear and a guest VLAN for visitors' devices. The home and lab
  networks hold dns01 and dns02, each running Technitium, Kea with a Stork agent, and
  PostgreSQL under Patroni in containers; docker01 with single sign-on and Ollama; the
  Proxmox cluster and the NAS; three Raspberry Pis; a secrets manager; and the step-ca
  private certificate authority.">
</picture>
<figcaption>What runs where. Some services are shy and aren't shown.</figcaption>
</figure>

## The rest of the house

Home Assistant runs alongside HomeKit (we're an Apple household). It's also what
finally got [my arcade cabinet]({{ '/2026/11/arcade-cabinet-home-assistant/' |
relative_url }}) to go to bed.

## The rules I try to hold it to

### Building it

- **If it isn't in Git, it isn't real.** Firewall rules, AWX settings, DNS zones and
  secrets policies are all code.
- **Terraform and Ansible both create things.** If I'm already using Ansible, I may
  stick with it all the way through. I'm pig-headed that way. Kubernetes stays with
  Helmfile.
- **Pick one way to do a thing.** On k3s, for example, Postgres runs under
  CloudNativePG.
- **Hostnames and ingress come with the workload.** On k3s and Docker alike, they're
  defined dynamically in the workload's own payload. No static assignments.

### Keeping the riff-raff out

- **Everything has a real, signed certificate.** step-ca internally, Let's Encrypt
  externally. Certificates are short-lived for almost everything.
- **Secrets stay out of the repo.** Workloads read them from the secrets manager, and
  the repos get scanned for leaks.
- **Single sign-on wherever it makes sense.** Nobody needs another password.
- **Scan what you build.** My own images get scanned, and anything left unfixed gets
  a reason and a review date.

### Keeping the lights on

- **Keep the shared pieces central.** DNS, DHCP, storage and virtualization are each
  handled in one place.
- **If the house leans on it, try to run two.** DNS, DHCP, the directory and the DMZ
  each come in pairs. Like socks, except these stay paired.
- **Back it up.** I try to make sure everything is backed up.
- **A backup doesn't count until it restores.** Until then it's just a hopeful file.
  There are restore tests for step-ca and Postgres.
- **Don't trust a success message.** The failure I keep hitting is a step that says
  it worked and did nothing. So check. Then maybe check the check.
- **A service isn't done until everything pointing at it is updated.** DNS,
  monitoring, sign-on, the dashboard and the docs, whether it's arriving or leaving.
- **Write it down so an agent can use it.** The documentation is structured so an AI
  agent can read it to check things and make changes.
