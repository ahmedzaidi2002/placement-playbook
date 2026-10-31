"""Clean redraws of the circuit figures in the Qualcomm core-subject questions.

Each function returns an SVG string. build.py writes them to
static/companies/qualcomm/core/<name>.svg. Where a photo was partly illegible the
figure is drawn as read, and the question text says so.
"""
from svg import Fig, ACCENT


def mux_dff():
    f = Fig(420, 175)
    f.text(10, 57, 'J', anchor='start', italic=True)
    f.text(10, 94, 'K', anchor='start', italic=True)
    ins, out, sel = f.mux(150, 20, 2, h=110, names=['0', '1'])
    f.wire((25, ins[0][1]), ins[0])
    gi, go = f.gate('not', 80, ins[1][1] - 20)
    f.wire((25, ins[1][1]), gi[0])
    f.wire(go, ins[1])
    p = f.box(250, 35, 80, 80, left=[('D', .3), ('CLK', .75)], right=[('Q', .3)], clock='CLK', title='D FF')
    f.hv(out, p['D'], mid=220)
    f.wire((222, p['CLK'][1]), p['CLK'])
    f.text(218, p['CLK'][1], 'CLK', anchor='end', size=11)
    q = p['Q']
    f.wire(q, (395, q[1]))
    f.text(405, q[1], 'Q', italic=True)
    f.dot(360, q[1])
    f.wire((360, q[1]), (360, 165), (sel[0][0], 165), sel[0])
    f.text(sel[0][0] + 8, 152, 'select', size=11, anchor='start')
    return f.svg()


def three_ff():
    f = Fig(400, 320)
    a = f.box(170, 10, 80, 70, title='D', above=True, left=[('D', .3), ('CLK', .75)], right=[('Q', .3)], clock='CLK')
    b = f.box(170, 115, 80, 70, title='T', above=True, left=[('T', .3), ('CLK', .75)], right=[('Q', .3)], clock='CLK')
    c = f.box(170, 220, 80, 90, title='JK', above=True, left=[('J', .22), ('CLK', .5), ('K', .78)], right=[('Q', .22)],
              clock='CLK')
    gi, go = f.gate('and', 90, a['D'][1] - 20)
    f.wire((60, gi[0][1]), gi[0]); f.text(52, gi[0][1], 'B', italic=True, anchor='end')
    f.wire((60, gi[1][1]), gi[1]); f.text(52, gi[1][1], 'C', italic=True, anchor='end')
    f.wire(go, a['D'])
    f.wire((130, b['T'][1]), b['T']); f.text(122, b['T'][1], '1', anchor='end')
    f.wire((110, c['J'][1]), c['J'])
    f.wire((110, c['K'][1]), c['K'])
    f.wire((110, c['J'][1]), (110, c['K'][1]))
    f.dot(110, c['J'][1]); f.dot(110, c['K'][1])
    f.wire((70, (c['J'][1] + c['K'][1]) / 2), (110, (c['J'][1] + c['K'][1]) / 2))
    f.text(62, (c['J'][1] + c['K'][1]) / 2, "B′", italic=True, anchor='end')
    for p in (a, b, c):
        f.wire((145, p['CLK'][1]), p['CLK'])
    f.wire((145, a['CLK'][1]), (145, 318))
    for p in (a, b):
        f.dot(145, p['CLK'][1])
    f.wire((145, 318), (40, 318)); f.text(32, 318, 'CLK', anchor='end', size=12)
    for p, n in ((a, 'A'), (b, 'B'), (c, 'C')):
        f.wire(p['Q'], (300, p['Q'][1]))
        f.text(312, p['Q'][1], n, italic=True)
    return f.svg()


def gates_p1q42():
    f = Fig(690, 300)
    A, B, Cy = 20, 75, 290
    f.text(10, A, 'A', italic=True, anchor='end'); f.text(10, B, 'B', italic=True, anchor='end')
    f.text(10, Cy, 'C', italic=True, anchor='end')
    g1i, g1o = f.gate('xor', 110, 45, label='G1')
    g2i, g2o = f.gate('xnor', 110, 125, label='G2')
    g3i, g3o = f.gate('and', 210, 85, n=3, h=60, label='G3')
    g4i, g4o = f.gate('xnor', 300, 65, label='G4')
    g5i, g5o = f.gate('or', 410, 25, label='G5')
    g6i, g6o = f.gate('xnor', 410, 115, label='G6')
    g7i, g7o = f.gate('xnor', 510, 60, n=3, h=60, label='G7')
    g8i, g8o = f.gate('xnor', 600, 80, label='G8')
    # A rail along the top
    f.wire((15, A), (390, A))
    f.dot(80, A); f.wire((80, A), (80, g1i[0][1]), g1i[0])
    f.wire((390, A), (390, g5i[0][1]), g5i[0])
    f.dot(375, A); f.wire((375, A), (375, g6i[0][1]), g6i[0])
    # B
    f.wire((15, B), (90, B), (90, g1i[1][1]), g1i[1])
    f.dot(60, B); f.wire((60, B), (60, g2i[0][1]), g2i[0])
    f.dot(40, B); f.wire((40, B), (40, 38), (285, 38), (285, g4i[0][1]), g4i[0])
    # C rail along the bottom
    f.wire((15, Cy), (585, Cy))
    f.dot(85, Cy); f.wire((85, Cy), (85, g2i[1][1]), g2i[1])
    f.dot(195, Cy); f.wire((195, Cy), (195, g3i[2][1]), g3i[2])
    f.dot(495, Cy); f.wire((495, Cy), (495, g7i[2][1]), g7i[2])
    f.wire((585, Cy), (585, g8i[1][1]), g8i[1])
    f.hv(g1o, g3i[0], mid=180)
    f.hv(g2o, g3i[1], mid=185)
    f.hv(g3o, g4i[1], mid=280)
    f.hv(g4o, g5i[1], mid=362)
    f.dot(362, g4o[1]); f.wire((362, g4o[1]), (362, g6i[1][1]), g6i[1])
    f.hv(g5o, g7i[0], mid=475)
    f.hv(g6o, g7i[1], mid=480)
    f.hv(g7o, g8i[0], mid=580)
    f.wire(g8o, (680, g8o[1])); f.text(690, g8o[1], 'F', italic=True)
    return f.svg()


def net_delay():
    f = Fig(360, 150)
    gi, go = f.gate('buf', 20, 30)
    f.wire((0, 50), gi[0])
    f.resistor(50, go[0], 150, label='R_net', horizontal=True)
    f.wire((150, 50), (260, 50))
    f.dot(170, 50)
    f.capacitor(170, 50, 120, label='C_net'); f.ground(170, 120)
    f.dot(240, 50)
    f.capacitor(240, 50, 120, label='C_pin'); f.ground(240, 120)
    bi, bo = f.gate('buf', 260, 30)
    f.wire(bo, (330, 50))
    f.text(36, 18, 'driver', size=11)
    f.text(275, 18, 'load gate', size=11)
    return f.svg()


def dtl_nand():
    f = Fig(450, 270)
    f.wire((150, 20), (360, 20)); f.supply(255, 20, '+5 V')
    f.resistor(150, 20, 115, label='6.8 kΩ')
    f.wire((150, 115), (150, 180))
    f.dot(150, 145); f.text(140, 145, 'P', anchor='end', italic=True)
    f.diode((150, 120), (60, 120), label='D_A', lside=-1)
    f.diode((150, 175), (60, 175), label='D_B', lside=1)
    f.wire((150, 115), (150, 120)); f.wire((150, 175), (150, 180))
    f.text(48, 120, 'A', italic=True, anchor='end'); f.text(48, 175, 'B', italic=True, anchor='end')
    f.wire((150, 145), (170, 145))
    f.diode((170, 145), (225, 145), label='D1')
    f.diode((230, 145), (285, 145), label='D2')
    f.wire((285, 145), (310, 145))
    f.dot(300, 145)
    f.resistor(300, 145, 235, label='6.8 kΩ', lx=250); f.ground(300, 235)
    q = f.npn(310, 145, label='Q1')
    f.resistor(q['c'][0], 20, 95, label='3.3 kΩ')
    f.wire((q['c'][0], 95), q['c'])
    f.dot(q['c'][0], 105); f.wire((q['c'][0], 105), (440, 105)); f.text(448, 105, 'Y', italic=True)
    f.wire(q['e'], (q['e'][0], 235)); f.ground(q['e'][0], 235)
    return f.svg()


def ring_states():
    import math
    f = Fig(360, 330)
    st = ['0001', '0010', '0100', '1000', '1001', '1100', '1110', '1111']
    cx, cy, R, r = 180, 165, 130, 27
    pts = []
    for i, s in enumerate(st):
        a = -math.pi / 2 + 2 * math.pi * i / len(st)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        pts.append((x, y))
        f.circle(x, y, r)
        f.text(x, y, s, size=12)
    for i in range(len(st)):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(st)]
        d = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        f.arrow((x1 + ux * r, y1 + uy * r), (x2 - ux * (r + 2), y2 - uy * (r + 2)))
    return f.svg()


def decoder_xor():
    f = Fig(420, 200)
    p = f.box(90, 10, 110, 170, title='74LS139', left=[('A', .25), ('B', .5), ("G′", .82)],
              right=[('Y0', .14), ('Y1', .38), ('Y2', .62), ('Y3', .86)], size=12)
    f.wire((40, p['A'][1]), p['A']); f.text(32, p['A'][1], 'A', italic=True, anchor='end')
    f.wire((40, p['B'][1]), p['B']); f.text(32, p['B'][1], 'B', italic=True, anchor='end')
    f.wire((60, p["G′"][1]), p["G′"]); f.text(52, p["G′"][1], '0', anchor='end')
    for k in ('Y1', 'Y2'):
        f.wire(p[k], (220, p[k][1]))
    f.text(145, 196, 'outputs are active-low', size=10)
    gi, go = f.gate('nor', 300, 70, inbub=True)
    f.hv(p['Y0'], gi[0], mid=255)
    f.hv(p['Y3'], gi[1], mid=265)
    f.wire(go, (395, go[1])); f.text(405, go[1], 'Y', italic=True)
    return f.svg()


def relay():
    f = Fig(330, 140)
    f.rect(30, 30, 70, 80, rx=4)
    d = 'M65,38'
    for i in range(4):
        d += f' a8,8 0 0 1 0,16'
    f.path(d)
    f.wire((30, 45), (50, 45), (50, 38), (65, 38)); f.wire((30, 95), (50, 95), (50, 102), (65, 102))
    f.text(65, 125, 'coil', size=11)
    f.wire((0, 45), (30, 45)); f.wire((0, 95), (30, 95))
    f.dot(200, 85); f.dot(280, 85)
    f.wire((200, 85), (272, 62))
    f.wire((200, 85), (200, 120)); f.wire((280, 85), (280, 120))
    f.wire((100, 70), (236, 70), dash=True)
    f.text(240, 125, 'one pole, one throw', size=11)
    return f.svg()


def ttl_nand():
    f = Fig(470, 300, pad=14)
    f.wire((150, 20), (360, 20)); f.supply(255, 20, '+5 V')
    f.resistor(150, 20, 120, label='R1 4 kΩ', lx=158)
    f.wire((150, 120), (150, 150)); f.dot(150, 150); f.text(158, 162, 'Y', italic=True, anchor='start')
    f.wire((150, 150), (120, 150), (120, 110), (115, 110)); f.wire((120, 150), (120, 190), (115, 190))
    f.diode((115, 110), (60, 110), label='D2', lside=-1)
    f.diode((115, 190), (60, 190), label='D3', lside=1)
    f.text(52, 110, 'A = +5 V', anchor='end', size=12)
    f.text(52, 190, 'B = 0 V', anchor='end', size=12)
    f.diode((150, 150), (225, 150), label='D4')
    q2 = f.npn(225, 150, label='Q2')
    x2 = q2['c'][0]
    f.resistor(x2, 20, 100, label='R2 1.6 kΩ', lx=x2 + 10)
    f.wire((x2, 100), q2['c'])
    f.dot(x2, 105)
    f.wire(q2['e'], (x2, 215)); f.dot(x2, 215)
    f.resistor(x2, 215, 280, label='R3 1 kΩ', lx=x2 - 62); f.ground(x2, 280)
    q3 = f.npn(330, 105, label='Q3')
    f.wire((x2, 105), (330, 105))
    x3 = q3['c'][0]
    f.resistor(x3, 20, 70, label='R4 130 Ω', lx=x3 + 10)
    f.wire((x3, 70), q3['c'])
    f.diode(q3['e'], (x3, 172), label='D1')
    q4 = f.npn(330, 215, label='Q4')
    f.wire((x2, 215), (330, 215))
    f.wire((x3, 172), q4['c'])
    f.dot(x3, 182); f.wire((x3, 182), (455, 182)); f.text(462, 182, 'X', italic=True)
    f.wire(q4['e'], (x3, 280)); f.ground(x3, 280)
    return f.svg()


def scan_chain():
    f = Fig(620, 190)
    q0 = sel0 = None
    for i, x in enumerate((60, 340)):
        ins, out, sel = f.mux(x, 30, 2, h=90, names=['0', '1'], title='')
        p = f.box(x + 90, 40, 70, 70, title='FF', above=True, left=[('D', .35), ('CLK', .78)], right=[('Q', .35)],
                  clock='CLK')
        f.hv(out, p['D'], mid=x + 65)
        f.wire((x + 75, p['CLK'][1]), p['CLK'])
        f.wire((x + 75, p['CLK'][1]), (x + 75, 175))
        f.wire(sel[0], (sel[0][0], 155))
        q = p['Q']
        if i == 0:
            f.wire(ins[0], (x - 30, ins[0][1])); f.text(x - 34, ins[0][1], 'D0', anchor='end', italic=True)
            f.wire(ins[1], (x - 30, ins[1][1])); f.text(x - 34, ins[1][1], 'SI', anchor='end', italic=True)
            f.wire(q, (x + 255, q[1]))
            f.text(x + 185, q[1] - 12, 'Q0', italic=True)
            q0, sel0 = (x + 255, q[1]), sel[0]
        else:
            f.wire((x - 10, 18), (x - 10, ins[0][1]), ins[0]); f.text(x - 10, 8, 'D1', italic=True)
            f.wire(q0, (x - 25, q0[1]), (x - 25, ins[1][1]), ins[1])
            f.wire(q, (x + 230, q[1]))
            f.text(x + 185, q[1] - 12, 'Q1', italic=True)
            f.wire((sel0[0], 155), (sel[0][0], 155))
    f.text(sel0[0] - 8, 155, 'S', anchor='end', italic=True)
    f.wire((135, 175), (415, 175)); f.text(127, 175, 'CLK', anchor='end', size=12)
    f.text(575, 52, '→ SO', size=12, anchor='start')
    return f.svg()


def sr_wave():
    f = Fig(470, 150)
    step = 65
    x0 = 50
    S = [(1, 1), (0, 1), (0, 1), (0, 1), (1, 1), (0, 1)]
    R = [(1, 1), (1, 1), (0, 1), (1, 1), (1, 1), (1, 1)]
    f.wave(x0, 30, S, step, name='S')
    f.wave(x0, 85, R, step, name='R')
    for i, n in enumerate('abcdefg'):
        x = x0 + i * step
        f.wire((x, 15), (x, 125), dash=True, color='#999')
        f.text(x, 140, n, italic=True)
    return f.svg()


def nmos_nand():
    f = Fig(260, 270)
    f.supply(120, 10, 'V_CC')
    f.resistor(120, 10, 80, label='R')
    f.wire((120, 80), (120, 95))
    f.dot(120, 95); f.wire((120, 95), (230, 95)); f.text(240, 95, 'Z', italic=True)
    q1 = f.nmos(58, 145, label='Q1')
    q2 = f.nmos(58, 220, label='Q2')
    f.wire((120, 95), (q1['d'][0], 95), q1['d'])
    f.wire(q1['s'], q2['d'])
    f.wire(q2['s'], (q2['s'][0], 262)); f.ground(q2['s'][0], 262)
    f.wire((20, 145), q1['g']); f.text(12, 145, 'A', italic=True, anchor='end')
    f.wire((20, 220), q2['g']); f.text(12, 220, 'B', italic=True, anchor='end')
    return f.svg()


def pla_or():
    """p3 Q44: one OR of three products."""
    f = Fig(490, 240)
    cols = ['A', "A′", 'B', "B′", 'C', "C′"]
    x0, dx = 50, 40
    for i, v in enumerate(cols):
        f.text(x0 + dx * i, 60, v, size=12, italic=True)
    f.text(x0 + dx * 2.5, 38, 'true and complemented input lines', size=10, color='#666')
    rows = [{'A', 'B', 'C'}, {"A′", 'B'}, {'A', 'B', "C′"}]
    gx = x0 + dx * 6
    outs = []
    for r, lits in enumerate(rows):
        y = 95 + 45 * r
        for i in range(6):
            f.wire((x0 + dx * i, 72), (x0 + dx * i, 215))
        f.wire((x0 - 15, y), (gx, y))
        for lit in lits:
            f.dot(x0 + dx * cols.index(lit), y, r=4)
        gi, go = f.gate('and', gx, y - 15, n=1, h=30)
        outs.append(go)
    gi, go = f.gate('or', 400, 110, n=3, h=60)
    for o, i in zip(outs, gi):
        f.hv(o, i, mid=375)
    f.wire(go, (470, go[1])); f.text(478, go[1], 'F', italic=True)
    return f.svg()


def sample_switch():
    f = Fig(340, 260)
    top, bot = f.source(40, 170, label='V_in')
    q = f.nmos(110, 130, label='M1')
    f.wire(top, (40, 60), (q['d'][0], 60), q['d'])
    f.wire((80, 130), q['g']); f.text(88, 114, 'V_G = +3 V', size=11)
    node = (q['s'][0], 200)
    f.wire(q['s'], node)
    f.wire(node, (300, 200)); f.text(306, 200, 'V_out', size=12, anchor='start')
    f.dot(250, 200)
    f.capacitor(250, 200, 248, label='C_H = 1 pF'); f.ground(250, 248)
    f.wire(bot, (40, 248)); f.ground(40, 248)
    return f.svg()


def jk_from_gates():
    f = Fig(470, 230)
    a1i, a1o = f.gate('and', 140, 20, n=3, h=54, label='Gate 1')
    a2i, a2o = f.gate('and', 140, 150, n=3, h=54, label='Gate 2')
    n3i, n3o = f.gate('nor', 260, 27, label='Gate 3')
    n4i, n4o = f.gate('nor', 260, 140, label='Gate 4')
    f.wire((40, a1i[1][1]), a1i[1]); f.text(32, a1i[1][1], 'K', italic=True, anchor='end')
    f.wire((40, a2i[1][1]), a2i[1]); f.text(32, a2i[1][1], 'J', italic=True, anchor='end')
    f.wire((40, 112), (110, 112)); f.text(32, 112, 'CLK', anchor='end', size=12)
    f.wire((110, a1i[2][1]), (110, a2i[0][1]))
    f.dot(110, 112)
    f.wire((110, a1i[2][1]), a1i[2]); f.wire((110, a2i[0][1]), a2i[0])
    f.hv(a1o, n3i[0], mid=225)
    f.hv(a2o, n4i[1], mid=225)
    q, qb = n3o, n4o
    f.wire(q, (440, q[1])); f.text(452, q[1], 'Q', italic=True)
    f.wire(qb, (440, qb[1])); f.text(454, qb[1], "Q′", italic=True)
    f.dot(330, q[1]); f.wire((330, q[1]), (330, 95), (245, 95), (245, n4i[0][1]), n4i[0])
    f.dot(345, qb[1]); f.wire((345, qb[1]), (345, 110), (238, 110), (238, n3i[1][1]), n3i[1])
    f.dot(400, q[1]); f.wire((400, q[1]), (400, 6), (125, 6), (125, a1i[0][1]), a1i[0])
    f.dot(415, qb[1]); f.wire((415, qb[1]), (415, 222), (125, 222), (125, a2i[2][1]), a2i[2])
    return f.svg()


def nand_or():
    f = Fig(300, 130)
    g1i, g1o = f.gate('nand', 70, 0)
    g2i, g2o = f.gate('nand', 70, 80)
    g3i, g3o = f.gate('nand', 190, 40)
    for gi, nm, y in ((g1i, 'A', 20), (g2i, 'B', 100)):
        f.wire((20, y), (55, y)); f.dot(55, y)
        f.wire((55, gi[0][1]), (55, gi[1][1]))
        f.wire((55, gi[0][1]), gi[0]); f.wire((55, gi[1][1]), gi[1])
        f.text(12, y, nm, italic=True, anchor='end')
    f.hv(g1o, g3i[0], mid=160)
    f.hv(g2o, g3i[1], mid=160)
    f.wire(g3o, (285, g3o[1])); f.text(295, g3o[1], 'Out', size=12)
    return f.svg()


def gates_p4q59():
    f = Fig(380, 150)
    o1i, o1o = f.gate('or', 70, 0)
    n1i, n1o = f.gate('not', 130, 0)
    a1i, a1o = f.gate('and', 70, 90)
    n2i, n2o = f.gate('not', 125, 90)
    a3i, a3o = f.gate('and', 215, 45)
    n3i, n3o = f.gate('not', 280, 45)
    f.wire((20, o1i[0][1]), o1i[0]); f.text(12, o1i[0][1], 'A', italic=True, anchor='end')
    f.wire((20, o1i[1][1]), o1i[1]); f.text(12, o1i[1][1], 'B', italic=True, anchor='end')
    f.dot(40, o1i[1][1]); f.wire((40, o1i[1][1]), (40, a1i[0][1]), a1i[0])
    f.wire((20, a1i[1][1]), a1i[1]); f.text(12, a1i[1][1], 'C', italic=True, anchor='end')
    f.wire(o1o, n1i[0]); f.wire(a1o, n2i[0])
    f.hv(n1o, a3i[0], mid=190); f.hv(n2o, a3i[1], mid=195)
    f.wire(a3o, n3i[0])
    f.wire(n3o, (365, n3o[1])); f.text(375, n3o[1], 'Y', italic=True)
    return f.svg()


def mux4():
    f = Fig(300, 200)
    ins, out, sel = f.mux(120, 0, 4, h=150, w=70, sel=2, names=['I0', 'I1', 'I2', 'I3'], title='4:1')
    for (x, y), v in zip(ins, '1001'):
        f.wire((60, y), (x, y)); f.text(50, y, v, anchor='end')
    f.wire(out, (230, out[1])); f.text(240, out[1], 'f', italic=True)
    for (x, y), nm, ly in zip(sel, ('S1 = A', 'S0 = B'), (180, 196)):
        f.wire((x, y), (x, ly - 8)); f.text(x, ly, nm, size=11)
    return f.svg()


def mod10():
    f = Fig(640, 230)
    boxes = []
    for i in range(4):
        x = 70 + 140 * i
        p = f.box(x, 30, 70, 80, title=f'FF{i}', above=True, left=[('J', .22), ('CLK', .5), ('K', .78)], right=[('Q', .22)],
                  bottom=[('CLR', .5)], clock='CLK', size=11)
        for k in ('J', 'K'):
            f.wire((x - 18, p[k][1]), p[k]); f.text(x - 22, p[k][1], '1', anchor='end', size=11)
        boxes.append(p)
    f.wire((20, boxes[0]['CLK'][1]), boxes[0]['CLK']); f.text(14, boxes[0]['CLK'][1], 'CLK', anchor='end', size=12)
    for i in range(3):
        q = boxes[i]['Q']
        nx = boxes[i + 1]['CLK']
        f.wire(q, (q[0] + 30, q[1]), (q[0] + 30, nx[1]), nx)
    for i, p in enumerate(boxes):
        q = p['Q']
        f.wire((q[0] + 15, q[1]), (q[0] + 15, 8)); f.dot(q[0] + 15, q[1])
        f.text(q[0] + 15, 0, f'Q{i}', italic=True, size=12)
    f.wire((612, boxes[3]['Q'][1]), boxes[3]['Q'])
    bus = 140
    f.wire((boxes[0]['CLR'][0], bus), (boxes[3]['CLR'][0], bus))
    for p in boxes:
        f.wire(p['CLR'], (p['CLR'][0], bus))
    gi, go = f.gate('and', 300, 170, label='')
    q1x = boxes[1]['Q'][0] + 15
    q3x = boxes[3]['Q'][0] + 15
    f.wire((q1x, 8), (q1x, 8))
    f.text(250, gi[0][1], 'Q1', italic=True, size=11, anchor='end')
    f.text(250, gi[1][1], 'Q3', italic=True, size=11, anchor='end')
    f.wire((255, gi[0][1]), gi[0]); f.wire((255, gi[1][1]), gi[1])
    f.wire(go, (370, go[1]), (370, bus)); f.dot(370, bus)
    return f.svg()


def pla_minterms():
    f = Fig(470, 420)
    cols = ['A', "A′", 'B', "B′", 'C', "C′"]
    x0, dx = 50, 36
    for i, v in enumerate(cols):
        f.text(x0 + dx * i, 8, v, size=12, italic=True)
        f.wire((x0 + dx * i, 18), (x0 + dx * i, 330))
    gx = x0 + dx * 6 + 10
    outs = []
    for m in range(8):
        y = 40 + 38 * m
        f.wire((x0 - 15, y), (gx, y))
        bits = [(m >> 2) & 1, (m >> 1) & 1, m & 1]
        for k, b in enumerate(bits):
            f.dot(x0 + dx * (2 * k + (0 if b else 1)), y, r=3.6)
        gi, go = f.gate('and', gx, y - 12, n=1, h=24)
        outs.append(go)
        f.text(gx + 14, y, f'm{m}', size=9)
    taps = {'F1': [0, 2], 'F2': [1, 4, 7]}
    for j, (nm, rows) in enumerate(taps.items()):
        lx = 360 + 55 * j
        f.wire((lx, 28), (lx, 345))
        for r in rows:
            y = outs[r][1]
            f.wire((lx - 5, y - 5), (lx + 5, y + 5), color=ACCENT)
            f.wire((lx - 5, y + 5), (lx + 5, y - 5), color=ACCENT)
        f.path(f'M{lx - 18},345 Q{lx},355 {lx + 18},345 Q{lx + 16},375 {lx},392 Q{lx - 16},375 {lx - 18},345 Z',
               fill='#fff')
        f.text(lx, 410, nm, italic=True)
    for go in outs:
        f.wire(go, (430, go[1]))
    return f.svg()


def gates_p5q55():
    f = Fig(450, 230, pad=45)
    g1i, g1o = f.gate('xor', 110, 0, label='XOR')
    g3i, g3o = f.gate('and', 110, 85, label='AND')
    g5i, g5o = f.gate('nor', 110, 170, label='NOR')
    g2i, g2o = f.gate('nand', 240, 30, label='NAND')
    g4i, g4o = f.gate('nand', 240, 130, label='NAND')
    qi, qo = f.gate('xor', 350, 80, label='XOR')
    f.text(20, 0, 'A = 1', size=12, anchor='end'); f.text(40, 0, '', size=1)
    f.wire((25, 0), (60, 0), (60, 215)); f.text(18, 0, '', size=1)
    f.wire((25, 20), (80, 20), (80, 225))
    f.text(20, 20, 'B = 0', size=12, anchor='end')
    for gi in (g1i, g3i, g5i):
        f.wire((60, gi[0][1]), gi[0]); f.dot(60, gi[0][1])
        f.wire((80, gi[1][1]), gi[1]); f.dot(80, gi[1][1])
    f.hv(g1o, g2i[0], mid=200)
    f.dot(200, g3o[1]); f.wire(g3o, (200, g3o[1]))
    f.wire((200, g3o[1]), (200, g2i[1][1]), g2i[1])
    f.wire((200, g3o[1]), (200, g4i[0][1]), g4i[0])
    f.hv(g5o, g4i[1], mid=215)
    f.hv(g2o, qi[0], mid=320)
    f.hv(g4o, qi[1], mid=320)
    f.wire(qo, (440, qo[1])); f.text(450, qo[1], 'Q', italic=True)
    return f.svg()


def ttl_not():
    f = Fig(470, 320)
    f.wire((140, 20), (360, 20)); f.supply(250, 20, 'V_CC = 5 V')
    f.resistor(170, 20, 120, label='4 kΩ', lx=130)
    # Q1 drawn sideways: emitter to the input on the left, collector to Q2's base
    f.wire((170, 120), (170, 160))
    f.wire((150, 160), (190, 160))
    f.arrow((158, 162), (128, 190))
    f.wire((182, 162), (212, 190))
    f.text(170, 182, 'Q1', size=12)
    f.wire((128, 190), (40, 190)); f.dot(40, 190); f.text(30, 190, 'V_i', anchor='end', size=12)
    q2 = f.npn(212, 190, label='Q2')
    x2 = q2['c'][0]
    f.resistor(x2, 20, 120, label='1.4 kΩ', lx=x2 - 58)
    f.wire((x2, 120), q2['c'])
    f.dot(x2, 128)
    f.wire(q2['e'], (x2, 250)); f.dot(x2, 250)
    f.resistor(x2, 250, 310, label='1 kΩ', lx=x2 - 48); f.ground(x2, 310)
    q4 = f.npn(310, 128, label='Q4')
    f.wire((x2, 128), (310, 128))
    x4 = q4['c'][0]
    f.resistor(x4, 20, 90, label='100 Ω', lx=x4 + 10)
    f.wire((x4, 90), q4['c'])
    f.diode(q4['e'], (x4, 205), label='D')
    q3 = f.npn(310, 250, label='Q3')
    f.wire((x2, 250), (310, 250))
    f.wire((x4, 205), q3['c'])
    f.dot(x4, 216); f.wire((x4, 216), (455, 216)); f.text(462, 216, 'V_o', size=12, anchor='start')
    f.wire(q3['e'], (x4, 310)); f.ground(x4, 310)
    return f.svg()


def sr_toggle():
    f = Fig(330, 170)
    p = f.box(110, 40, 90, 90, left=[('S', .2), ('R', .8)], right=[('Q', .2), ("Q′", .8)], size=13)
    cy = 85
    f.text(126, cy, 'CLK', size=11, anchor='start')
    f.wire((110, cy - 7), (120, cy), (110, cy + 7))
    f.circle(105, cy, 5)
    f.wire((40, cy), (100, cy)); f.text(32, cy, 'CLK', anchor='end', size=12)
    q, qb = p['Q'], p["Q′"]
    f.wire(q, (310, q[1])); f.text(318, q[1], '?', size=15, bold=True)
    f.wire(qb, (260, qb[1]))
    f.dot(240, qb[1]); f.wire((240, qb[1]), (240, 8), (90, 8), (90, p['S'][1]), p['S'])
    f.dot(275, q[1]); f.wire((275, q[1]), (275, 160), (80, 160), (80, p['R'][1]), p['R'])
    return f.svg()


def sipo():
    f = Fig(500, 230)
    f.rect(60, 10, 340, 70)
    f.text(230, 30, 'Serial-in parallel-out register', size=13, bold=True)
    xs = {'D3': 110, 'D2': 160, 'D1': 260, 'D0': 310}
    for n, x in xs.items():
        f.text(x, 62, n, size=12)
        f.wire((x, 80), (x, 100))
    f.wire((20, 40), (60, 40)); f.text(14, 40, 'CLK', anchor='end', size=12)
    x1i, x1o = f.gate('xor', 190, 160)
    n1i, n1o = f.gate('nand', 330, 110)
    x2i, x2o = f.gate('xor', 420, 140)
    f.wire((110, 100), (110, x1i[0][1]), x1i[0])
    f.wire((160, 100), (160, x1i[1][1]), x1i[1])
    f.wire((260, 100), (260, n1i[0][1]), n1i[0])
    f.wire((310, 100), (310, n1i[1][1]), n1i[1])
    f.hv(n1o, x2i[0], mid=398)
    f.wire(x1o, (405, x1o[1]), (405, x2i[1][1]), x2i[1])
    f.wire(x2o, (482, x2o[1]), (482, 45))
    f.arrow((482, 45), (402, 45))
    f.text(445, 32, 'serial in X', size=11)
    return f.svg()


def or_of_inverted():
    f = Fig(260, 130)
    gi, go = f.gate('or', 150, 10, n=3, h=110)
    for (x, y), nm in zip(gi, 'ABC'):
        ni, no = f.gate('not', 70, y - 13, h=26)
        f.wire((20, y), ni[0]); f.text(12, y, nm, italic=True, anchor='end')
        f.wire(no, (x, y))
    f.wire(go, (245, go[1])); f.text(255, go[1], 'Y', italic=True)
    return f.svg()


def clock_gating():
    f = Fig(640, 330)
    gi, go = f.gate('and', 120, 0)
    f.wire((60, gi[0][1]), gi[0]); f.text(52, gi[0][1], 'Gate', anchor='end', size=12)
    f.wire((60, gi[1][1]), gi[1]); f.text(52, gi[1][1], 'CLK', anchor='end', size=12)
    p = f.box(260, 0, 100, 60, title='FF', left=[('clk', 1 / 3)], clock='clk', size=11)
    f.wire(go, p['clk'])
    s = 2
    rows = [
        ('CLK', [(0, 61), (1, 56), (0, 58), (1, 55), (0, 45)]),
        ('Gate', [(1, 72), (0, 115), (1, 88)]),
        ('clk at FF', [(0, 61), (1, 11), (0, 115), (1, 43), (0, 45)]),
        ('A gating', [(1, 54), (0, 115), (1, 106)]),
        ('B gating', [(0, 54), (1, 116), (0, 105)]),
    ]
    y = 80
    for name, lv in rows:
        f.wave(100, y, lv, s, h=24, name=name, color=ACCENT if name == 'clk at FF' else None)
        y += 50
    f.text(100 + 66 * s, 70 + 2 * 50 + 40, 'glitch', size=11, color=ACCENT)
    return f.svg()


def tristate_mux():
    f = Fig(380, 170)
    i1, o1, e1 = f.tristate(150, 20)
    i0, o0, e0 = f.tristate(150, 100, up=False)
    f.wire((40, i1[1]), i1); f.text(32, i1[1], 'In1', anchor='end', size=12)
    f.wire((40, i0[1]), i0); f.text(32, i0[1], 'In0', anchor='end', size=12)
    f.wire((40, 160), (110, 160)); f.text(32, 160, 'X', italic=True, anchor='end')
    f.dot(90, 160)
    f.wire((90, 160), (90, 8), (e1[0], 8), e1)
    ni, no = f.gate('not', 110, 140)
    f.wire(no, (e0[0], 160), e0)
    f.wire(o1, (220, o1[1]), (220, o0[1]), o0)
    f.dot(220, 75)
    bi, bo = f.gate('buf', 260, 55)
    f.wire((220, 75), bi[0])
    f.wire(bo, (350, 75)); f.text(362, 75, 'Out', size=12)
    return f.svg()


def demux_block():
    f = Fig(300, 170)
    f.rect(110, 10, 80, 120)
    f.text(150, 70, 'X', size=18, bold=True)
    f.wire((40, 70), (110, 70)); f.text(32, 70, 'in', anchor='end', size=12)
    for i in range(4):
        y = 10 + 120 * (i + 1) / 5
        f.wire((190, y), (260, y)); f.text(270, y, f'Y{i}', size=12, anchor='start')
    for x in (135, 165):
        f.wire((x, 130), (x, 160))
    f.text(150, 168, 'control lines', size=11)
    return f.svg()


def lockup_pair():
    f = Fig(300, 110)
    for x, s in ((60, '1010'), (240, '0101')):
        f.circle(x, 55, 32)
        f.text(x, 55, s, size=14)
    f.path('M92,45 Q150,10 208,45')
    f.arrow((200, 40), (208, 45))
    f.path('M208,65 Q150,100 92,65')
    f.arrow((100, 70), (92, 65))
    f.text(150, 18, 'clock', size=11)
    f.text(150, 95, 'clock', size=11)
    return f.svg()


ALL = {
    'mux-dff': mux_dff, 'three-ff': three_ff, 'gates-p1q42': gates_p1q42, 'net-delay': net_delay,
    'dtl-nand': dtl_nand, 'ring-states': ring_states, 'decoder-xor': decoder_xor, 'relay': relay,
    'ttl-nand': ttl_nand, 'scan-chain': scan_chain, 'sr-wave': sr_wave, 'nmos-nand': nmos_nand,
    'pla-or': pla_or, 'sample-switch': sample_switch, 'jk-from-gates': jk_from_gates, 'nand-or': nand_or,
    'gates-p4q59': gates_p4q59, 'mux4': mux4, 'mod10': mod10,
    'pla-minterms': pla_minterms, 'gates-p5q55': gates_p5q55, 'ttl-not': ttl_not, 'sr-toggle': sr_toggle,
    'sipo': sipo, 'or-of-inverted': or_of_inverted, 'clock-gating': clock_gating, 'tristate-mux': tristate_mux,
    'demux-block': demux_block, 'lockup-pair': lockup_pair,
}
