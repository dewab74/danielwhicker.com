"""Draws the stacked "how it fits together" diagram into services-*.svg.

Run from this folder: python3 network.py
"""

from proxmox import PAD, ROW, SPACE, THEMES, W, rect, text

GAP = 10
THIRD = (W - 2 * PAD - 2 * GAP) / 3  # three columns inside the inside-network panel


def box(c, x, y, w, name, role="", h=ROW, fill=None, ink=None):
    fill, ink = fill or c["vm"], ink or c["vm_text"]
    edge = c["vm_edge"] if fill == c["vm"] else None
    out, mid = [rect(x, y, w, h, fill, edge)], x + w / 2
    if role:
        out += [text(mid, y + h / 2 - 3, name, ink, 14, True),
                text(mid, y + h / 2 + 14, role, ink, 12)]
    else:
        out.append(text(mid, y + h / 2 + 5, name, ink, 14, True))
    return out


def row(c, y, items, widths, x=PAD):
    out = []
    for (name, role), w in zip(items, widths):
        out += box(c, x, y, w, name, role)
        x += w + GAP
    return out


def draw(c):
    out = [text(W / 2, 22, "How it fits together", c["text"], 18, True)]
    out.append(f'<path d="M1 48V40H{W - 1}V48M{W / 2} 40V30" fill="none" stroke="{c["line"]}"/>')
    y = 58

    # In from outside: top to bottom.
    for label, fill, ink in (("Internet", c["panel"], c["text"]),
                             ("OPNsense firewall and router", c["cp"], c["on"])):
        out.append(rect(0, y, W, 40, fill, c["edge"]))
        out.append(text(W / 2, y + 25, label, ink, 15, True))
        y += 48

    # The networks the firewall keeps apart.
    dmz_w = 475
    half = (dmz_w - 2 * PAD - GAP) / 2
    dmz_h = 36 + 2 * ROW + SPACE + PAD
    out.append(rect(0, y, dmz_w, dmz_h, c["panel"], c["edge"], 6))
    out.append(text(dmz_w / 2, y + 24, "DMZ VLAN: published services", c["text"], 15, True))
    out += row(c, y + 36, [("edge-proxy-1", "edge proxy"), ("edge-proxy-2", "edge proxy")],
               [half, half])
    out += row(c, y + 36 + ROW + SPACE,
               [("bastion-1", "SSH bastion"), ("bastion-2", "SSH bastion")], [half, half])
    side_x, side_w, side_h = dmz_w + 15, W - dmz_w - 15, (dmz_h - 12) / 2
    for i, (name, role) in enumerate((("IoT VLAN", "smart home gear"),
                                      ("Guest VLAN", "visitors' devices"))):
        top = y + i * (side_h + 12)
        out.append(rect(side_x, top, side_w, side_h, c["panel"], c["edge"], 6))
        out.append(text(side_x + side_w / 2, top + side_h / 2 - 4, name, c["text"], 15, True))
        out.append(text(side_x + side_w / 2, top + side_h / 2 + 15, role, c["text"], 12))
    y += dmz_h + 12

    # Everything inside.
    host_h = 34 + 3 * ROW + 2 * SPACE + PAD
    height = 38 + host_h + 3 * (ROW + GAP) + PAD
    out.append(rect(0, y, W, height, c["panel"], c["edge"], 6))
    out.append(text(W / 2, y + 25, "Home and lab networks", c["text"], 15, True))
    y += 38
    hosts = (
        ("dns01: containers", [("DNS01", "Technitium primary"), ("DHCP01", "Kea, Stork agent"),
                               ("PostgreSQL", "under Patroni")]),
        ("dns02: containers", [("DNS02", "Technitium secondary"), ("DHCP02", "Kea, Stork agent"),
                               ("PostgreSQL", "under Patroni")]),
        ("docker01: containers", [("Single sign-on", ""), ("Ollama", "local LLM")]),
    )
    for i, (title, items) in enumerate(hosts):
        x = PAD + i * (THIRD + GAP)
        out.append(rect(x, y, THIRD, host_h, c["panel"], c["vm_edge"], 6))
        out.append(text(x + THIRD / 2, y + 22, title, c["text"], 14, True))
        top = y + host_h - PAD / 2 - len(items) * ROW - (len(items) - 1) * SPACE
        for name, role in items:
            out += box(c, x + PAD / 2, top, THIRD - PAD, name, role)
            top += ROW + SPACE
    y += host_h + GAP
    two = 2 * THIRD + GAP
    out += box(c, PAD, y, two, "Proxmox cluster", "pve01, pve02, pve03: k3s and other VMs",
               fill=c["wk"], ink=c["on"])
    out += box(c, PAD + two + GAP, y, THIRD, "NAS", "disks, volumes and files",
               fill=c["wk"], ink=c["on"])
    y += ROW + GAP
    out += row(c, y, [("dns0q", "Pi: Patroni witness"), ("rpi-usbip", "Pi: print and scan"),
                      ("Batocera", "Pi: arcade and retro games")], [THIRD] * 3)
    y += ROW + GAP
    wide = (W - 2 * PAD - GAP) / 2
    out += row(c, y, [("Secrets manager", ""), ("step-ca", "private certificate authority")],
               [wide, wide])
    total = int(y + ROW + PAD + 1)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {total}" '
            f'width="{W}" height="{total}" font-family="Helvetica, Arial, sans-serif">\n'
            + "\n".join(out) + "\n</svg>\n"), total


if __name__ == "__main__":
    for name, colors in THEMES.items():
        svg, h = draw(colors)
        with open(f"services-{name}.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print("services", name, W, h)
