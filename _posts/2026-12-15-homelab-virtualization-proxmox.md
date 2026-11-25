---
layout: post
date: 2026-12-15 09:00:00 -0600
title: "Homelab: virtualization on Proxmox"
description: "Why I left VMware, what runs where, and how the VMs get built."
accent: infrastructure
tags: [homelab, proxmox, packer, ansible]
series: homelab
series_part: 2
---

## So long, VMware, and thanks for all the VMs

It started out running ESXi and vCenter, where I tested automated VMware
deployments, among other things.

Then came the Broadcom acquisition. Licensing, no access to VMware updates, blah
blah blah. Today it runs Proxmox. I even did the move in place, as a rolling
migration with Ansible.

I migrated all the VMs to a NAS share (they were on vSAN!), tore down vSAN, drained
a node, and reimaged it with Proxmox. Then I imported a clone of the hosts' VMs into
Proxmox, onto a new Proxmox share on the NAS.

## Who lives where

Three little boxes doing their best: pve01, pve02 and pve03. Storage is their local
disks plus the NAS.

Each node is an Intel NUC with 64GB of RAM. Which isn't enough. It's never enough.
And now it's worth its weight in platinum.

<figure>
<picture>
<source media="(prefers-color-scheme: dark)"
  srcset="{{ '/assets/img/homelab/proxmox-dark.svg' | relative_url }}">
<img src="{{ '/assets/img/homelab/proxmox-light.svg' | relative_url }}"
  width="720" height="523" loading="lazy"
  alt="A stacked diagram of the Proxmox cluster. Three columns, pve01, pve02 and pve03,
  each hold a k3s control plane VM and a k3s worker VM. Above those, pve01 has idm01 and
  lab VMs, pve02 has Home Assistant and lab VMs, and pve03 has idm02. Under all three run
  layers for the network, storage, and Proxmox VE on three mini PCs.">
</picture>
<figcaption>The seating chart. The two directory servers keep their distance.</figcaption>
</figure>

## Where VMs come from

- **Templates.** Packer bakes them: RHEL, Rocky, Ubuntu and Windows Server. CI
  builds the Linux cloud images and checks that a clone of each one works.
- **One inventory.** There's an entry per VM, and it's the source of truth for what
  each one is made of. If it isn't in the file, it's a rumor.
- **Lifecycle.** Ansible handles it, from clone to power button, with migration,
  configuration and disks along the way.
