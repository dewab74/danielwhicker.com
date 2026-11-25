---
layout: post
date: 2026-12-22 09:00:00 -0600
title: "Homelab: Kubernetes on k3s"
description: "Six VMs, what runs on them, and a plan to move the workers onto metal."
accent: infrastructure
tags: [homelab, kubernetes, k3s, helmfile]
series: homelab
series_part: 3
---

## Yes, Kubernetes, at home

Most applications run on k3s, because of course they do. There are three control
plane VMs and three workers, one of each pinned to every Proxmox node: k3s-m01 to
m03 and k3s-n01 to n03.

<figure>
<picture>
<source media="(prefers-color-scheme: dark)"
  srcset="{{ '/assets/img/homelab/k3s-dark.svg' | relative_url }}">
<img src="{{ '/assets/img/homelab/k3s-light.svg' | relative_url }}"
  width="720" height="845" loading="lazy"
  alt="A stacked diagram of the k3s cluster. Application groups sit on top. Automation:
  AWX and ARC. Monitoring: Prometheus, Grafana, Loki and Uptime Kuma. Alerts and chat:
  Matrix, Hookshot and mailrise. Records: Wiki.js and NetBox. Data: CloudNativePG and
  SeaweedFS. DHCP and tools: Stork, Headlamp and SearXNG. Under them are layers for
  traffic, names and certificates, and storage. At the bottom, each Proxmox node holds one
  worker VM and one control plane VM running kube-vip.">
</picture>
<figcaption>Inside the cluster. Where each lands is the scheduler's business.</figcaption>
</figure>

- kube-vip holds the control plane's address, MetalLB hands out service addresses,
  and NGINX works the front door.
- external-dns writes the DNS records for whatever gets published, so I don't have
  to.
- cert-manager and step-issuer get certificates from step-ca, my private
  certificate authority.
- Most volumes live on the NAS over NFS. Postgres runs under CloudNativePG.
- Helmfile deploys the workloads.
- Ansible builds and upgrades the cluster, one node at a time, with a fork of
  k3s-ansible.

## Robots doing chores

- **AWX** runs the scheduled and self-healing Ansible jobs, and its own
  configuration is code too. Turtles most of the way down.
- **ARC** runs GitHub Actions runners in the cluster, from a custom image with
  Ansible, Packer and Terraform in it.

## Who watches the watchers?

Prometheus, Grafana, Loki and Uptime Kuma. Alerts go to self-hosted Matrix rooms,
one per service, so they stay out of my real mail. My inbox is grateful.

## Next up: bare metal

The plan is to slowly move the k3s workers off VMs and onto physical MicroOS boxes.
