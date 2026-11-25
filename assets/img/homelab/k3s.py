"""Draws the stacked k3s diagram. Run from this folder: python3 k3s.py"""

from proxmox import COL, GAP, HEAD, PAD, ROW, SPACE, THEMES, W, block, rect, text

# Application groups, three to a row, then the platform layers underneath them.
GROUPS = [
    [
        ("Automation", [("AWX", "Ansible jobs and events"),
                        ("ARC", "GitHub Actions runners")]),
        ("Monitoring", [("Prometheus", "with Alertmanager"), ("Grafana", "dashboards"),
                        ("Loki", "logs, via Alloy, Promtail"),
                        ("Uptime Kuma", "up or down")]),
        ("Alerts and chat", [("Matrix", "with Element"), ("Hookshot", "webhooks"),
                             ("mailrise", "email to chat")]),
    ],
    [
        ("Records", [("Wiki.js", "documentation"), ("NetBox", "inventory")]),
        ("Data", [("CloudNativePG", "Postgres"), ("SeaweedFS", "object storage")]),
        ("DHCP and tools", [("Stork", "DHCP management"), ("Headlamp", "cluster UI"),
                            ("SearXNG", "search")]),
    ],
]
LAYERS = [
    "Traffic: NGINX ingress and MetalLB",
    "Names and certificates: external-dns, cert-manager, step-ca via step-issuer",
    "Storage: NFS CSI to the NAS, and local-path",
]


def draw(c):
    out = [text(W / 2, 22, "k3s cluster", c["text"], 18, True)]
    out.append(f'<path d="M1 48V40H{W - 1}V48M{W / 2} 40V30" fill="none" stroke="{c["line"]}"/>')
    y = 58
    for row in GROUPS:
        tallest = max(len(items) for _, items in row)
        body = tallest * ROW + (tallest - 1) * SPACE
        height = HEAD + body + PAD
        for i, (title, items) in enumerate(row):
            x = i * (COL + GAP)
            out.append(rect(x, y, COL, height, c["panel"], c["edge"], 6))
            out.append(text(x + COL / 2, y + 24, title, c["text"], 15, True))
            top = y + HEAD + body - len(items) * (ROW + SPACE) + SPACE
            for name, role in items:
                out += block(x + PAD, top, name, role, c["vm"], c["vm_text"], c["vm_edge"])
                top += ROW + SPACE
        y += height + 12
    for label in LAYERS:
        out.append(rect(0, y, W, 40, c["bar"], c["edge"]))
        out.append(text(W / 2, y + 25, label, c["bar_text"], 15, True))
        y += 48
    # The base: one worker and one control plane VM on each Proxmox node.
    base = HEAD + 2 * ROW + SPACE + PAD
    for i in range(3):
        x, n = i * (COL + GAP), i + 1
        out.append(rect(x, y, COL, base, c["panel"], c["edge"], 6))
        out += block(x + PAD, y + PAD, f"k3s-n0{n}", "worker", c["wk"], c["on"])
        out += block(x + PAD, y + PAD + ROW + SPACE, f"k3s-m0{n}", "control plane, kube-vip",
                     c["cp"], c["on"])
        out.append(text(x + COL / 2, y + base - 12, f"VMs on pve0{n}", c["text"], 14, True))
    height = y + base + 1
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" '
            f'width="{W}" height="{height}" font-family="Helvetica, Arial, sans-serif">\n'
            + "\n".join(out) + "\n</svg>\n"), height


if __name__ == "__main__":
    for name, colors in THEMES.items():
        svg, h = draw(colors)
        with open(f"k3s-{name}.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print("k3s", name, W, h)
