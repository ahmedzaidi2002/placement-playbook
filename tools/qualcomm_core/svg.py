"""Tiny schematic kit: logic gates, flip-flop boxes, discrete parts and waveforms as SVG.

Every helper appends SVG elements to a Fig and returns the pin coordinates the caller
needs for wiring. Coordinates are plain user units; Fig.svg() sizes the viewBox to fit.
Black on white, so the figures read the same in light and dark mode (the page puts a
white card behind every .nb-fig image).
"""
import math

STROKE = '#1f2328'
ACCENT = '#c2185b'
FONT = "font-family='Helvetica, Arial, sans-serif'"


class Fig:
    def __init__(self, w, h, pad=10):
        self.w, self.h, self.pad = w, h, pad
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def svg(self):
        p = self.pad
        return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='{-p} {-p} {self.w + 2 * p} {self.h + 2 * p}' "
                f"width='{self.w + 2 * p}' height='{self.h + 2 * p}'>"
                f"<rect x='{-p}' y='{-p}' width='{self.w + 2 * p}' height='{self.h + 2 * p}' fill='#fff'/>"
                f"<g fill='none' stroke='{STROKE}' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'>"
                + ''.join(self.parts) + '</g></svg>')

    # ---- primitives ---------------------------------------------------------------
    def wire(self, *pts, color=None, dash=False):
        d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        extra = f" stroke='{color}'" if color else ''
        if dash:
            extra += " stroke-dasharray='5 4'"
        self.add(f"<polyline points='{d}'{extra}/>")

    def hv(self, a, b, mid=None):
        """Orthogonal wire a -> b: horizontal, vertical at x=mid (default halfway), horizontal."""
        (x1, y1), (x2, y2) = a, b
        if abs(y1 - y2) < 0.01:
            self.wire(a, b)
            return
        m = (x1 + x2) / 2 if mid is None else mid
        self.wire(a, (m, y1), (m, y2), b)

    def dot(self, x, y, r=3):
        self.add(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{STROKE}' stroke='none'/>")

    def text(self, x, y, s, size=13, anchor='middle', italic=False, bold=False, color=None):
        st = " font-style='italic'" if italic else ''
        st += " font-weight='bold'" if bold else ''
        s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        if '_' in s:  # V_CC -> V with subscript CC (up to the next space)
            head, tail = s.split('_', 1)
            sub, _, rest = tail.partition(' ')
            s = (f"{head}<tspan font-size='{size * 0.72:.1f}' dy='4'>{sub}</tspan>"
                 + (f"<tspan dy='-4'> {rest}</tspan>" if rest else ''))
        self.add(f"<text x='{x:.1f}' y='{y:.1f}' {FONT} font-size='{size}' text-anchor='{anchor}' "
                 f"dominant-baseline='middle' fill='{color or STROKE}' stroke='none'{st}>{s}</text>")

    def rect(self, x, y, w, h, fill='#fff', dash=False, rx=0):
        d = " stroke-dasharray='5 4'" if dash else ''
        self.add(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='{fill}'{d}/>")

    def circle(self, x, y, r, fill='#fff'):
        self.add(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{fill}'/>")

    def path(self, d, fill='none'):
        self.add(f"<path d='{d}' fill='{fill}'/>")

    def arrow(self, a, b, color=None):
        (x1, y1), (x2, y2) = a, b
        self.wire(a, b, color=color)
        ang = math.atan2(y2 - y1, x2 - x1)
        L = 8
        p1 = (x2 - L * math.cos(ang - 0.4), y2 - L * math.sin(ang - 0.4))
        p2 = (x2 - L * math.cos(ang + 0.4), y2 - L * math.sin(ang + 0.4))
        c = color or STROKE
        self.add(f"<polygon points='{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}' "
                 f"fill='{c}' stroke='{c}'/>")

    # ---- logic gates ----------------------------------------------------------------
    def gate(self, kind, x, y, n=2, h=40, inbub=False, label=None):
        """Gate body with its back edge at x, top at y. Returns (inputs, output).
        kind: and nand or nor xor xnor not buf."""
        kind = kind.lower()
        neg = kind in ('nand', 'nor', 'xnor', 'not')
        base = {'nand': 'and', 'nor': 'or', 'xnor': 'xor', 'not': 'buf'}.get(kind, kind)
        cy = y + h / 2
        if base == 'buf':
            self.path(f'M{x},{y + 4} L{x + 30},{cy} L{x},{y + h - 4} Z', fill='#fff')
            out = (x + 30, cy)
            ins = [(x, cy)]
        elif base == 'and':
            r = h / 2
            self.path(f'M{x},{y} H{x + 20} A{r},{r} 0 0 1 {x + 20},{y + h} H{x} Z', fill='#fff')
            out = (x + 20 + r, cy)
            ins = [(x, y + h * (i + 1) / (n + 1)) for i in range(n)]
        else:  # or / xor
            k = 12
            self.path(f'M{x},{y} Q{x + k},{cy} {x},{y + h} Q{x + 28},{y + h} {x + 46},{cy} '
                      f'Q{x + 28},{y} {x},{y} Z', fill='#fff')
            out = (x + 46, cy)
            back = x - 7 if base == 'xor' else x
            if base == 'xor':
                self.path(f'M{back},{y} Q{back + k},{cy} {back},{y + h}')
            ins = []
            for i in range(n):
                s = (i + 1) / (n + 1)
                ins.append((back + 2 * k * s * (1 - s), y + h * s))
        if neg:
            self.circle(out[0] + 4, out[1], 4)
            out = (out[0] + 8, out[1])
        if inbub:
            new = []
            for px, py in ins:
                self.circle(px - 4, py, 4)
                new.append((px - 8, py))
            ins = new
        if label:
            self.text(x + 18, y + h + 10, label, size=11, color='#666')
        return ins, out

    def tristate(self, x, y, h=30, up=True):
        """Buffer with an enable on its top (up) or bottom. Returns (in, out, enable)."""
        cy = y + h / 2
        self.path(f'M{x},{y} L{x + 26},{cy} L{x},{y + h} Z', fill='#fff')
        en = (x + 13, y + h / 4) if up else (x + 13, y + 3 * h / 4)
        return (x, cy), (x + 26, cy), en

    # ---- blocks -----------------------------------------------------------------------
    def box(self, x, y, w, h, title=None, left=(), right=(), top=(), bottom=(), clock=None, size=12,
            above=False):
        """Rectangle with named pins. Pins are lists of names (evenly spaced) or (name, frac).
        clock: name of a left pin drawn with the edge triangle. Returns dict name -> (x, y)."""
        self.rect(x, y, w, h)
        if title:
            ty = y - 10 if above else y + h / 2
            self.text(x + w / 2, ty, title, size=size, bold=True)
        pins = {}

        def place(names, side):
            for i, nm in enumerate(names):
                if isinstance(nm, tuple):
                    nm, f = nm
                else:
                    f = (i + 1) / (len(names) + 1)
                if side == 'l':
                    px, py = x, y + h * f
                    self.text(px + (14 if nm == clock else 6), py, nm, size=size, anchor='start')
                elif side == 'r':
                    px, py = x + w, y + h * f
                    self.text(px - 6, py, nm, size=size, anchor='end')
                elif side == 't':
                    px, py = x + w * f, y
                    self.text(px, py + 11, nm, size=size)
                else:
                    px, py = x + w * f, y + h
                    self.text(px, py - 11, nm, size=size)
                if nm == clock and side == 'l':
                    self.wire((x, py - 6), (x + 9, py), (x, py + 6))
                pins[nm] = (px, py)

        place(left, 'l')
        place(right, 'r')
        place(top, 't')
        place(bottom, 'b')
        return pins

    def mux(self, x, y, n_in, h=None, w=40, sel=1, names=None, title='MUX'):
        """Trapezoid MUX. Returns (inputs, output, select pins on the bottom edge)."""
        h = h or 30 * n_in + 10
        self.path(f'M{x},{y} L{x + w},{y + 12} L{x + w},{y + h - 12} L{x},{y + h} Z', fill='#fff')
        ins = [(x, y + h * (i + 1) / (n_in + 1)) for i in range(n_in)]
        for i, (px, py) in enumerate(ins):
            self.text(px + 5, py, names[i] if names else str(i), size=11, anchor='start')
        out = (x + w, y + h / 2)
        sels = []
        for i in range(sel):
            fx = x + w * (i + 1) / (sel + 1)
            fy = y + h - 12 * (fx - x) / w
            sels.append((fx, fy))
        if title:
            self.text(x + w / 2 + 2, y + h / 2, title, size=9)
        return ins, out, sels

    # ---- discrete parts (vertical unless noted) ------------------------------------------
    def resistor(self, x, y1, y2, label=None, horizontal=False, lx=None):
        """Zig-zag between (x,y1) and (x,y2), or along x from y1 to y2 at height x if horizontal."""
        n, amp = 6, 6
        if horizontal:
            yy, xa, xb = x, y1, y2
            L = xb - xa
            s0, s1 = xa + L * 0.2, xb - L * 0.2
            pts = [(xa, yy), (s0, yy)]
            for i in range(n):
                pts.append((s0 + (s1 - s0) * (i + 0.5) / n, yy + (amp if i % 2 else -amp)))
            pts += [(s1, yy), (xb, yy)]
            self.wire(*pts)
            if label:
                self.text((xa + xb) / 2, yy - 15, label, size=12)
            return
        L = y2 - y1
        s0, s1 = y1 + L * 0.2, y2 - L * 0.2
        pts = [(x, y1), (x, s0)]
        for i in range(n):
            pts.append((x + (amp if i % 2 else -amp), s0 + (s1 - s0) * (i + 0.5) / n))
        pts += [(x, s1), (x, y2)]
        self.wire(*pts)
        if label:
            self.text(lx if lx is not None else x + 12, (y1 + y2) / 2, label, size=12, anchor='start')

    def capacitor(self, x, y1, y2, label=None, horizontal=False):
        if horizontal:
            yy, xa, xb = x, y1, y2
            m = (xa + xb) / 2
            self.wire((xa, yy), (m - 4, yy))
            self.wire((m + 4, yy), (xb, yy))
            self.wire((m - 4, yy - 12), (m - 4, yy + 12))
            self.wire((m + 4, yy - 12), (m + 4, yy + 12))
            if label:
                self.text(m, yy - 20, label, size=12)
            return
        m = (y1 + y2) / 2
        self.wire((x, y1), (x, m - 4))
        self.wire((x, m + 4), (x, y2))
        self.wire((x - 12, m - 4), (x + 12, m - 4))
        self.wire((x - 12, m + 4), (x + 12, m + 4))
        if label:
            self.text(x + 16, m, label, size=12, anchor='start')

    def inductor(self, xa, xb, y, label=None):
        n = 4
        seg = (xb - xa) / (n + 2)
        d = f'M{xa},{y} H{xa + seg}'
        for i in range(n):
            x0 = xa + seg * (i + 1)
            d += f' A{seg / 2},{seg / 2} 0 0 1 {x0 + seg},{y}'
        d += f' H{xb}'
        self.path(d)
        if label:
            self.text((xa + xb) / 2, y - 18, label, size=12)

    def ground(self, x, y):
        self.wire((x, y), (x, y + 6))
        self.wire((x - 10, y + 6), (x + 10, y + 6))
        self.wire((x - 6, y + 10), (x + 6, y + 10))
        self.wire((x - 2, y + 14), (x + 2, y + 14))

    def supply(self, x, y, label):
        self.wire((x - 10, y), (x + 10, y))
        self.text(x, y - 10, label, size=12)

    def diode(self, a, b, label=None, lside=1):
        """Diode from anode a to cathode b (any direction)."""
        (x1, y1), (x2, y2) = a, b
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        px, py = -uy, ux
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        t0 = (mx - 7 * ux, my - 7 * uy)
        t1 = (mx + 7 * ux, my + 7 * uy)
        self.wire(a, t0)
        self.wire(t1, b)
        self.add(f"<polygon points='{t0[0] + 8 * px:.1f},{t0[1] + 8 * py:.1f} {t0[0] - 8 * px:.1f},{t0[1] - 8 * py:.1f} "
                 f"{t1[0]:.1f},{t1[1]:.1f}' fill='#fff'/>")
        self.wire((t1[0] + 8 * px, t1[1] + 8 * py), (t1[0] - 8 * px, t1[1] - 8 * py))
        if label:
            self.text(mx + lside * 18 * px, my + lside * 18 * py, label, size=12)

    def npn(self, x, y, label=None, size=22, emitter_down=True):
        """NPN with base at (x, y). Returns dict base, c, e (collector up, emitter down)."""
        bx = x + 14
        self.wire((x, y), (bx, y))
        self.wire((bx, y - size * 0.6), (bx, y + size * 0.6))
        c = (bx + size, y - size)
        e = (bx + size, y + size)
        self.wire((bx, y - size * 0.3), c)
        self.arrow((bx, y + size * 0.3), (e[0] - 2, e[1] - 2))
        if label:
            self.text(bx + size + 6, y, label, size=12, anchor='start')
        return {'b': (x, y), 'c': c, 'e': e}

    def nmos(self, x, y, label=None, h=36):
        """NMOS with gate wire ending at (x, y). Drain on top, source at bottom."""
        gx = x + 14
        self.wire((x, y), (gx, y))
        self.wire((gx, y - h / 2), (gx, y + h / 2))
        cx = gx + 6
        self.wire((cx, y - h / 2), (cx, y + h / 2))
        d = (cx + 22, y - h / 2 - 14)
        s = (cx + 22, y + h / 2 + 14)
        self.wire((cx, y - h / 2 + 4), (d[0], y - h / 2 + 4), d)
        self.wire((cx, y + h / 2 - 4), (s[0], y + h / 2 - 4), s)
        self.arrow((s[0], y + h / 2 - 4), (cx + 4, y + h / 2 - 4))
        if label:
            self.text(d[0] + 8, y, label, size=12, anchor='start')
        return {'g': (x, y), 'd': d, 's': s}

    def source(self, x, y, r=16, label=None, ac=True):
        self.circle(x, y, r)
        if ac:
            self.path(f'M{x - 9},{y} C{x - 5},{y - 9} {x - 1},{y - 9} {x},{y} C{x + 1},{y + 9} {x + 5},{y + 9} {x + 9},{y}')
        else:
            self.text(x, y - 6, '+', size=12)
            self.text(x, y + 7, '−', size=12)
        if label:
            self.text(x - r - 6, y, label, size=12, anchor='end')
        return (x, y - r), (x, y + r)

    # ---- waveforms ------------------------------------------------------------------------
    def wave(self, x0, y0, levels, step, h=22, name=None, color=None):
        """Digital waveform; levels is a list of (value, length_in_steps)."""
        pts = []
        x = x0
        prev = None
        for v, n in levels:
            yy = y0 + (0 if v else h)
            if prev is not None and prev != yy:
                pts.append((x, prev))
            pts.append((x, yy))
            x += n * step
            pts.append((x, yy))
            prev = yy
        self.wire(*pts, color=color)
        if name:
            self.text(x0 - 10, y0 + h / 2, name, size=12, anchor='end')
        return x
