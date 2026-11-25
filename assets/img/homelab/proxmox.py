"""Draws the stacked Proxmox cluster diagram. Run from this folder: python3 proxmox.py"""

from html import escape

NODES = {  # node: VMs above the k3s pair, top to bottom
    "pve01": [("idm01", "directory"), ("Lab VMs", "")],
    "pve02": [("Home Assistant", ""), ("Lab VMs", "")],
    "pve03": [("idm02", "directory")],
}
THEMES = {
    "light": dict(text="#152544", line="#4B5D77", panel="#E9EFF8", edge="#C5D0E0",
                  vm="#FFFFFF", vm_edge="#9FB0CB", vm_text="#152544",
                  cp="#006477", wk="#1658A6", on="#FFFFFF", bar="#374965", bar_text="#FFFFFF"),
    "dark": dict(text="#F1F5F9", line="#94A3B8", panel="#0B1B40", edge="#34496B",
                 vm="#20365C", vm_edge="#4B628A", vm_text="#F1F5F9",
                 cp="#22D3EE", wk="#60A5FA", on="#050F2D", bar="#14294F", bar_text="#F1F5F9"),
}
W, COL, GAP, ROW, SPACE, PAD = 720, 230, 15, 48, 8, 10
HEAD, TOP = 36, 58
ROWS = max(len(v) for v in NODES.values()) + 2


def rect(x, y, w, h, fill, edge=None, r=4):
    stroke = f' stroke="{edge}"' if edge else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{stroke}/>'


def text(x, y, s, fill, size=14, bold=False):
    weight = ' font-weight="700"' if bold else ""
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}"{weight} '
            f'text-anchor="middle">{escape(s)}</text>')


def block(x, y, name, role, fill, ink, edge=None):
    w = COL - 2 * PAD
    out = [rect(x, y, w, ROW, fill, edge)]
    mid = x + w / 2
    if role:
        out += [text(mid, y + 21, name, ink, 14, True), text(mid, y + 38, role, ink, 12)]
    else:
        out.append(text(mid, y + 29, name, ink, 14, True))
    return out


def draw(c):
    body_h = ROWS * ROW + (ROWS - 1) * SPACE + SPACE
    col_h = HEAD + body_h + PAD
    out = [text(W / 2, 22, "Proxmox cluster", c["text"], 18, True)]
    out.append(f'<path d="M1 48V40H{W - 1}V48M{W / 2} 40V30" fill="none" stroke="{c["line"]}"/>')
    for i, (node, vms) in enumerate(NODES.items()):
        x = i * (COL + GAP)
        out.append(rect(x, TOP, COL, col_h, c["panel"], c["edge"], 6))
        out.append(text(x + COL / 2, TOP + 24, node, c["text"], 15, True))
        bottom = TOP + HEAD + body_h
        n = i + 1
        cp_y = bottom - ROW
        wk_y = cp_y - ROW - SPACE
        out += block(x + PAD, cp_y, f"k3s-m0{n}", "k3s control plane", c["cp"], c["on"])
        out += block(x + PAD, wk_y, f"k3s-n0{n}", "k3s worker", c["wk"], c["on"])
        y = wk_y - SPACE * 2 - len(vms) * (ROW + SPACE) + SPACE
        for name, role in vms:
            out += block(x + PAD, y, name, role, c["vm"], c["vm_text"], c["vm_edge"])
            y += ROW + SPACE
    y = TOP + col_h + 12
    for label in ("Network: OPNsense and the switch", "Storage: local disks and the NAS"):
        out.append(rect(0, y, W, 40, c["bar"], c["edge"]))
        out.append(text(W / 2, y + 25, label, c["bar_text"], 15, True))
        y += 48
    out.append(rect(0, y, W, 86, c["panel"], c["edge"], 6))
    out.append(text(W / 2, y + 25, "Three mini PCs", c["text"], 15, True))
    out.append(rect(PAD, y + 38, W - 2 * PAD, 38, c["cp"]))
    out.append(text(W / 2, y + 62, "Proxmox VE", c["on"], 15, True))
    height = y + 87
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" '
            f'width="{W}" height="{height}" font-family="Helvetica, Arial, sans-serif">\n'
            + "\n".join(out) + "\n</svg>\n"), height


if __name__ == "__main__":
    for name, colors in THEMES.items():
        svg, h = draw(colors)
        with open(f"proxmox-{name}.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print("proxmox", name, W, h)
