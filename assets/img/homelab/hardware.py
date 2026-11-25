"""Draws the stacked hardware diagram. Run from this folder: python3 hardware.py"""

from proxmox import COL, GAP, HEAD, PAD, SPACE, THEMES, W, rect, text

# Machines, three columns: title, then (name, detail lines) top to bottom.
COLUMNS = [
    ("Proxmox cluster", [("pve01", ["mini PC"]), ("pve02", ["mini PC"]),
                         ("pve03", ["mini PC"])]),
    ("DNS and DHCP", [("dns01", ["mini PC"]), ("dns02", ["mini PC"])]),
    ("Storage and containers", [
        ("docker01", ["mini PC"]),
        ("NAS", ["Terramaster F6-424", "4 x 20 TB in two mirrors", "1 TB NVMe cache"]),
    ]),
]
PIS = [("dns0q", "tie-breaker"), ("rpi-usbip", "print and scan"), ("Batocera", "arcade and retro games")]


def box_height(lines):
    return 31 + 17 * len(lines)


def box(c, x, y, w, name, lines):
    mid = x + w / 2
    out = [rect(x, y, w, box_height(lines), c["vm"], c["vm_edge"]),
           text(mid, y + 21, name, c["vm_text"], 14, True)]
    out += [text(mid, y + 38 + 17 * i, line, c["vm_text"], 12) for i, line in enumerate(lines)]
    return out


def draw(c):
    out = [text(W / 2, 22, "Hardware", c["text"], 18, True)]
    out.append(f'<path d="M1 48V40H{W - 1}V48M{W / 2} 40V30" fill="none" stroke="{c["line"]}"/>')

    # Row one: the machines, bottom-aligned like the other diagrams.
    y = 58
    bodies = [sum(box_height(d) for _, d in items) + SPACE * (len(items) - 1)
              for _, items in COLUMNS]
    body = max(bodies)
    height = HEAD + body + PAD
    for i, (title, items) in enumerate(COLUMNS):
        x = i * (COL + GAP)
        out.append(rect(x, y, COL, height, c["panel"], c["edge"], 6))
        out.append(text(x + COL / 2, y + 24, title, c["text"], 15, True))
        top = y + HEAD + body - bodies[i]
        for name, lines in items:
            out += box(c, x + PAD, top, COL - 2 * PAD, name, lines)
            top += box_height(lines) + SPACE
    y += height + 12

    # Row two: the Raspberry Pis, with what hangs off one of them, and wireless.
    wide = 2 * COL + GAP
    small = (wide - 2 * PAD - 2 * SPACE) / 3
    one = box_height([""])
    drop = 26
    height = HEAD + 2 * one + drop + PAD
    out.append(rect(0, y, wide, height, c["panel"], c["edge"], 6))
    out.append(text(wide / 2, y + 24, "Raspberry Pis", c["text"], 15, True))
    top = y + HEAD
    for i, (name, role) in enumerate(PIS):
        out += box(c, PAD + i * (small + SPACE), top, small, name, [role])
    mid, under = wide / 2, top + one + drop
    left, right = mid - (small + SPACE) / 2, mid + (small + SPACE) / 2
    out.append(f'<path d="M{mid} {top + one}V{under - 13}M{left} {under}V{under - 13}H{right}V{under}" '
               f'fill="none" stroke="{c["line"]}" stroke-width="1.5"/>')
    out += box(c, left - small / 2, under, small, "Laser printer", ["Dell, on USB"])
    out += box(c, right - small / 2, under, small, "Scanner", ["on USB"])
    x = 2 * (COL + GAP)
    out.append(rect(x, y, COL, height, c["panel"], c["edge"], 6))
    out.append(text(x + COL / 2, y + 24, "Wireless", c["text"], 15, True))
    out += box(c, x + PAD, y + HEAD + (height - HEAD - PAD - one) / 2, COL - 2 * PAD,
               "Access points", ["three of them"])
    y += height + 12

    # Shared layers: everything above plugs into the switch.
    for label, fill, ink in (("28-port managed switch", c["bar"], c["bar_text"]),
                             ("OPNsense firewall and router, on a mini PC", c["cp"], c["on"]),
                             ("Internet", c["panel"], c["text"])):
        out.append(rect(0, y, W, 40, fill, c["edge"]))
        out.append(text(W / 2, y + 25, label, ink, 15, True))
        y += 48
    total = y - 7
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {total}" '
            f'width="{W}" height="{total}" font-family="Helvetica, Arial, sans-serif">\n'
            + "\n".join(out) + "\n</svg>\n"), total


if __name__ == "__main__":
    for name, colors in THEMES.items():
        svg, h = draw(colors)
        with open(f"hardware-{name}.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print("hardware", name, W, h)
