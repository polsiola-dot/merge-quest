# Adds ids, idle loops, a "director" timeline of signature moves and tap
# reactions to the converted cast, producing homecast/scene.rml.
import re, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
rml = open(os.path.join(HERE, 'cast.rml')).read()
FPS = 60
deg = math.pi / 180

# ---------- ids on the named nodes ----------
nid = [8000]
ids = {}
def add_id(m):
    name = m.group(2)
    if re.fullmatch(r'(two|four|purple|eight)(_[A-Za-z0-9]+)?', name) and name not in ids:
        nid[0] += 1; ids[name] = f'0:{nid[0]}'
        return f'{m.group(1)}name="{name}" id="{ids[name]}"'
    return m.group(0)
rml = re.sub(r'(<(?:Node|Shape)[^>]*?)name="([^"]+)"', add_id, rml)
# Clip shapes come out as fixed top-level nodes; move each one next to the
# group it clips (same body coordinates) so it travels with its buddy.
for m in list(re.finditer(r'        <Node [^>]*name="(clip-[^"]+)" id="([^"]+)">\n(.*?)\n        </Node>\n', rml, re.S)):
    rml = rml.replace(m.group(0), '')
    clip = f'<Node name="{m.group(1)}" id="{m.group(2)}">\n{m.group(3)}\n</Node>\n'
    at = rml.index(f'<ClippingShape sourceId="{m.group(2)}"')
    g = rml.rindex('<Node name="Group">', 0, at)
    rml = rml[:g] + clip + rml[g:]
# start values of every node we key
base = {}
for m in re.finditer(r'<(?:Node|Shape)([^>]*?)name="([^"]+)" id="([^"]+)"', rml):
    attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
    base[m.group(2)] = {k: float(attrs.get(k, d)) for k, d in
                        [('x', 0), ('y', 0), ('rotation', 0), ('scaleX', 1), ('scaleY', 1), ('opacity', 1)]}
# effect parts start hidden
for n in ['eight_aura', 'four_zz', 'four_yawn', 'purple_spark0', 'purple_spark1', 'purple_spark2']:
    rml = rml.replace(f'name="{n}" id="{ids[n]}"', f'opacity="0" name="{n}" id="{ids[n]}"'); base[n]['opacity'] = 0
# artboard style + default state machine
rml = re.sub(r'<Artboard width="800" height="600" name="HomeCast" id="([^"]+)">',
             lambda m: f'<Artboard defaultStateMachineId="0:9002" styleId="0:9003" clip="true" width="800" height="600" name="HomeCast" id="{m.group(1)}">\n'
                       '        <LayoutComponentStyle name="Artboard Style" id="0:9003"/>', rml, count=1)
scale = {n: base[n + '_bob']['scaleX'] for n in ['two', 'four', 'purple', 'eight']}
R = {'two': 10, 'four': 10, 'eight': 10, 'purple': 12}
SHUT = {'two': 2.1, 'four': 1.3, 'purple': 2.1, 'eight': 1.6}

# ---------- tracks ----------
# A track is {(node, prop): [(t_seconds, value, ease)]}; ease 'io' | 'out' | 'lin' | 'hold'
class Clip:
    def __init__(self): self.k = {}
    def key(self, node, prop, t, v, ease='io'):
        self.k.setdefault((node, prop), []).append((t, v, ease))
    def rest(self, node, prop):
        return base[node][prop]
    def path(self, node, prop, t0, pts, ease='io', rel=True):
        """pts: [(dt, value-offset)], keys at t0+dt; offsets add to the rest value."""
        r = self.rest(node, prop) if rel else 0
        for dt, v in pts: self.key(node, prop, t0 + dt, r + v, ease)
    def merge(self, other, t0=0):
        for kp, ks in other.k.items():
            for t, v, e in ks: self.key(*kp, t + t0, v, e)

EASES = {'io': (0.42, 0, 0.58, 1), 'out': (0, 0, 0.58, 1), 'in': (0.42, 0, 1, 1)}
def keyframes_xml(ks, dur_frames, loop_rest=None):
    ks = sorted(ks, key=lambda k: k[0])
    out, last = [], None
    for t, v, e in ks:
        f = min(round(t * FPS), dur_frames)
        if last is not None and f == last: continue   # one key per frame
        last = f
        if e == 'hold': out.append(f'<KeyFrameDouble value="{v:.4f}" frame="{f}" interpolationType="hold"/>')
        elif e == 'lin': out.append(f'<KeyFrameDouble value="{v:.4f}" frame="{f}" interpolationType="linear"/>')
        else:
            x1, y1, x2, y2 = EASES[e]
            out.append(f'<KeyFrameDouble value="{v:.4f}" frame="{f}" interpolationType="cubic"><CubicEaseInterpolator x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/></KeyFrameDouble>')
    return '\n'.join(out)

anims = []   # (name, id, xml)
aid = [9100]
def animation(name, clip, dur, loop=False):
    aid[0] += 1; a = f'0:{aid[0]}'
    F = round(dur * FPS); objs = {}
    for (node, prop), ks in clip.k.items():
        r = base[node][prop]
        ks = list(ks)
        if loop or True:   # every track starts and ends at rest
            if min(k[0] for k in ks) > 0: ks.append((0, r, 'io'))
            if max(k[0] for k in ks) < dur: ks.append((dur, r, 'io'))
        objs.setdefault(node, []).append(f'<KeyedProperty property="{prop}">\n{keyframes_xml(ks, F)}\n</KeyedProperty>')
    body = '\n'.join(f'<KeyedObject objectId="{ids[n]}">\n' + '\n'.join(ps) + '\n</KeyedObject>' for n, ps in objs.items())
    anims.append((name, a, f'<LinearAnimation {"loopValue=\"loop\" " if loop else ""}duration="{F}" name="{name}" id="{a}">\n{body}\n</LinearAnimation>'))
    return a

# ---------- building blocks ----------
def blink(c, n, t, ms=180, hold=0, depth=1, eyes='LR', node='lid'):
    d = R[n] * SHUT[n] * depth; a = ms / 2000; h = hold / 1000
    for e in eyes:
        nd = f'{n}_{node}{e}'
        c.path(nd, 'y', t, [(0, 0), (a, d), (a + h, d), (2 * a + h, 0)])
def look(c, n, t, x, y, dur=1.4, node='pupL', both=True):
    for e in ('L', 'R'):
        nd = f'{n}_pup{e}' + ('s' if node.endswith('s') else '')
        c.path(nd, 'x', t, [(0, 0), (dur * .15, x), (dur * .85, x), (dur, 0)])
        c.path(nd, 'y', t, [(0, 0), (dur * .15, y), (dur * .85, y), (dur, 0)])

# signature moves (clip, duration)
def sig_two():
    c = Clip(); a = 'two_act'
    look(c, 'two', 0, 0, -3.5, 1.3, node='s')
    c.path(a, 'y', 0, [(0, 0), (.39, -16), (.72, 0)], 'out')
    c.path(a, 'rotation', 0, [(0, 0), (.39, -6 * deg), (.72, -10 * deg), (1.1, -10 * deg), (1.3, 0)])
    return c, 1.4
def sig_four_yawn():
    c = Clip(); a = 'four_act'
    blink(c, 'four', 0, 700, 1100, .85, node='lid', eyes='LR') if False else None
    d = R['four'] * SHUT['four'] * .85
    for e in 'LR': c.path(f'four_lid{e}s', 'y', 0, [(0, 0), (.35, d), (1.45, d), (1.8, 0)])
    c.path(a, 'scaleX', 0, [(0, 0), (.66, -.04), (1.24, -.04), (1.56, .06), (1.9, 0)])
    c.path(a, 'scaleY', 0, [(0, 0), (.66, .08), (1.24, .08), (1.56, -.08), (1.9, 0)])
    c.path('four_smile', 'opacity', 0, [(0, 0), (.28, -1), (1.52, -1), (1.9, 0)])
    c.path('four_yawn', 'opacity', 0, [(0, 0), (.57, 1), (1.33, 1), (1.9, 0)])
    c.path('four_yawn', 'scaleX', 0, [(0, -.7), (.57, 0), (1.33, 0), (1.9, -.7)])
    c.path('four_yawn', 'scaleY', 0, [(0, -.7), (.57, 0), (1.33, 0), (1.9, -.7)])
    return c, 2.0
def sig_four_doze():
    c = Clip(); a = 'four_act'
    d = R['four'] * SHUT['four']
    for e in 'LR': c.path(f'four_lid{e}s', 'y', 0, [(0, 0), (.5, d), (3.9, d), (3.95, -R['four'] * .5), (4.6, -R['four'] * .5), (4.8, 0)])
    c.path(a, 'rotation', 0, [(0, 0), (.6, 4 * deg), (3.9, 4 * deg), (4.0, 0)])
    c.path(a, 'y', 0, [(0, 0), (.6, 2), (3.9, 2), (4.05, -12), (4.32, 0)], 'out')
    c.path(a, 'scaleY', 0, [(0, 0), (3.9, 0), (4.05, .06), (4.32, 0)])
    for t0 in (0.5, 1.75, 3.0):   # three z's float up one after another
        c.path('four_zz', 'opacity', t0, [(0, 0), (.35, 1), (1.15, 0)], 'lin')
        c.path('four_zz', 'x', t0, [(0, 0), (1.15, 10)], 'out'); c.path('four_zz', 'x', t0 + 1.15, [(.05, 0)], 'hold')
        c.path('four_zz', 'y', t0, [(0, 0), (1.15, -22)], 'out'); c.path('four_zz', 'y', t0 + 1.15, [(.05, 0)], 'hold')
        c.path('four_zz', 'scaleX', t0, [(0, -.4), (1.15, .2)], 'lin'); c.path('four_zz', 'scaleY', t0, [(0, -.4), (1.15, .2)], 'lin')
    return c, 5.0
def sig_purple(wink=False):
    c = Clip(); a = 'purple_act'
    c.path(a, 'y', 0, [(0, 0), (.33, -20), (.6, 0), (.82, -9), (1.1, 0)])
    for e, s in (('L', -1), ('R', 1)):
        c.path(f'purple_arm{e}s', 'rotation', 0, [(0, 0), (.27, 18 * s * deg), (.55, -10 * s * deg), (.82, 18 * s * deg), (1.1, 0)])
    for i in range(3):
        t0 = .25 + i * .16; nd = f'purple_spark{i}'
        c.path(nd, 'opacity', t0, [(0, 0), (.4, 1), (.8, 0)], 'lin')
        c.path(nd, 'scaleX', t0, [(0, -.8), (.4, .1), (.8, -.6)]); c.path(nd, 'scaleY', t0, [(0, -.8), (.4, .1), (.8, -.6)])
        c.path(nd, 'rotation', t0, [(0, 0), (.8, 60 * deg)], 'lin')
    if wink:
        d = R['purple'] * SHUT['purple']
        c.path('purple_lidRs', 'y', 1.2, [(0, 0), (.19, d), (.39, d), (.58, 0)])
        return c, 1.9
    return c, 1.7
def sig_eight():
    c = Clip(); a = 'eight_act'
    d = R['eight'] * SHUT['eight'] * .32
    for e in 'LR': c.path(f'eight_lid{e}s', 'y', 0, [(0, 0), (.25, d), (1.15, d), (1.4, 0)])
    c.path(a, 'x', 0, [(0, 0), (.15, -1.5), (.3, 1.5), (.45, -1.5), (.6, 0)], 'lin')
    c.path(a, 'scaleX', 0, [(0, 0), (.6, 0), (.75, .08), (1.02, -.06), (1.27, .02), (1.5, 0)])
    c.path(a, 'scaleY', 0, [(0, 0), (.6, 0), (.75, -.1), (1.02, .1), (1.27, -.02), (1.5, 0)])
    c.path(a, 'y', 0, [(0, 0), (.75, 0), (1.02, -6), (1.27, 0)])
    c.path('eight_aura', 'opacity', 0, [(0, 0), (.75, 0), (1.05, 1), (1.5, 0)])
    c.path('eight_aura', 'scaleX', 0, [(0, -.2), (1.05, 0), (1.5, .15)], 'lin'); c.path('eight_aura', 'scaleY', 0, [(0, -.2), (1.05, 0), (1.5, .15)], 'lin')
    return c, 1.6
def glance(n, toward_right, t=.25, dur=1.6):
    c = Clip(); look(c, n, t, 3.5 if toward_right else -3.5, -1, dur, node='s'); return c

ORDER_X = {'two': 0, 'four': 1, 'purple': 2, 'eight': 3}   # left → right
def with_glance(clip_dur, who, neighbour):
    c, d = clip_dur
    c.merge(glance(neighbour, ORDER_X[who] > ORDER_X[neighbour]))
    return c, max(d, 1.9)

# ---------- director: signature moves in turn, irregular gaps (60 s loop) ----------
director = Clip()
plan = [(4.0, with_glance(sig_two(), 'two', 'four')),
        (11.0, with_glance(sig_purple(), 'purple', 'two')),
        (19.5, with_glance(sig_eight(), 'eight', 'purple')),
        (26.0, sig_four_yawn()),
        (33.5, with_glance(sig_two(), 'two', 'purple')),
        (40.5, with_glance(sig_purple(True), 'purple', 'eight')),
        (48.0, with_glance(sig_four_doze(), 'four', 'two')),
        (56.0, sig_eight())]
for t0, (c, d) in plan: director.merge(c, t0)
DIRECTOR = animation('Signature moves (auto)', director, 60.0, loop=True)

# ---------- idle loops: bob (short) + blinks/looks (long, different lengths) ----------
def bob(n, dur, pts_y, rot=None, sx=None):
    c = Clip(); s = scale[n]; nd = f'{n}_bob'
    c.path(nd, 'y', 0, [(t * dur, v * s) for t, v in pts_y])
    if rot: c.path(nd, 'rotation', 0, [(t * dur, v * deg) for t, v in rot])
    if sx: 
        c.path(nd, 'scaleX', 0, [(t * dur, v * s) for t, v in sx]); c.path(nd, 'scaleY', 0, [(t * dur, -v * s) for t, v in sx])
    return c
idle = {}
idle['two'] = (bob('two', 1.5, [(0, 0), (.5, -5), (1, 0)]), 1.5)
idle['four'] = (bob('four', 3.8, [(0, 0), (.5, -3), (1, 0)], sx=[(0, 0), (.5, .01), (1, 0)]), 3.8)
pb = bob('purple', 1.8, [(0, 0), (.25, -8), (.5, 0), (.75, -8), (1, 0)], rot=[(0, 0), (.25, -3), (.5, 0), (.75, 3), (1, 0)])
pb.path('purple_armL', 'rotation', 0, [(0, 0), (.9, -9 * deg), (1.8, 0)]); pb.path('purple_armR', 'rotation', 0, [(0, 0), (.9, 9 * deg), (1.8, 0)])
idle['purple'] = (pb, 1.8)
idle['eight'] = (bob('eight', 3.0, [(0, 0), (.5, -3), (1, 0)]), 3.0)

eyes = {}
c = Clip()   # curious: quick blinks every 2-4 s, some doubles; pupils dart around
for t, dbl in [(1.2, False), (3.4, True), (6.9, False), (9.1, True), (12.0, False), (14.3, False), (17.6, True)]:
    blink(c, 'two', t, 140)
    if dbl: blink(c, 'two', t + .23, 140)
for t, x, y, d in [(.4, 3, -2, 1.0), (2.2, -3.5, 1, .8), (4.6, 2.5, -3.5, 1.5), (7.8, -2.5, -3, 1.1), (10.2, 3.5, 1.5, .9), (13.1, -3, -1, 1.4), (16.0, 1.5, -3.5, 1.0)]:
    look(c, 'two', t, x, y, d, node='')
eyes['two'] = (c, 19.3)
c = Clip()   # sleepy: slow heavy blinks every 4-7 s
for t in [2.0, 7.4, 12.1, 18.6]: blink(c, 'four', t, 560, 220)
eyes['four'] = (c, 23.9)
c = Clip()   # cheerful: every 3-5 s, sometimes a wink
for t, w in [(1.5, ''), (5.2, 'R'), (8.4, ''), (12.9, ''), (16.3, 'L')]:
    blink(c, 'purple', t, 380 if w else 180, 160 if w else 0, eyes=w or 'LR')
eyes['purple'] = (c, 19.9)
c = Clip()   # determined: rare, firm snaps
for t in [3.1, 9.6, 16.8]: blink(c, 'eight', t, 110)
eyes['eight'] = (c, 22.1)

IDLE = {n: animation(f'{n} idle', *idle[n], loop=True) for n in idle}
EYES = {n: animation(f'{n} eyes', *eyes[n], loop=True) for n in eyes}
REST = animation('rest', Clip(), 0.1)
TAP = {'two': [animation('two tap', *with_glance(sig_two(), 'two', 'four'))],
       'four': [animation('four tap (yawn)', *sig_four_yawn()), animation('four tap (doze)', *sig_four_doze())],
       'purple': [animation('purple tap', *with_glance(sig_purple(True), 'purple', 'eight'))],
       'eight': [animation('eight tap', *with_glance(sig_eight(), 'eight', 'purple'))]}

# ---------- state machine ----------
sid = [9500]
def nxt(): sid[0] += 1; return f'0:{sid[0]}'
layers, inputs, listeners = [], [], []
def loop_layer(name, anim, x):
    s = nxt(); L = nxt()
    return (f'<StateMachineLayer name="{name}" id="{L}"><AnyState x="{x}" y="-120"/><ExitState x="{x+200}" y="-120"/>'
            f'<EntryState x="{x}" y="0"><StateTransition stateToId="{s}"/></EntryState>'
            f'<AnimationState x="{x}" y="120" animationId="{anim}" id="{s}"/></StateMachineLayer>')
for n in ['two', 'four', 'purple', 'eight']:
    layers.append(loop_layer(f'{n} bob', IDLE[n], 0)); layers.append(loop_layer(f'{n} blinks', EYES[n], 0))
layers.append(loop_layer('auto moves', DIRECTOR, 0))
for n in ['two', 'four', 'purple', 'eight']:
    trig = nxt(); inputs.append(f'<StateMachineTrigger name="tap {n}" id="{trig}"/>')
    rest = nxt(); L = nxt(); sts = []
    outs = ''
    for i, a in enumerate(TAP[n]):
        s = nxt()
        outs += f'<StateTransition stateToId="{s}"><TransitionTriggerCondition inputId="{trig}"/></StateTransition>'
        sts.append(f'<AnimationState x="{i*220}" y="260" animationId="{a}" reset="true" id="{s}">'
                   f'<StateTransition stateToId="{rest}" enableExitTime="true" exitTimeIsPercetange="true" exitTime="100"/></AnimationState>')
    layers.append(f'<StateMachineLayer name="{n} tap" id="{L}"><AnyState x="0" y="-120"/><ExitState x="200" y="-120"/>'
                  f'<EntryState x="0" y="0"><StateTransition stateToId="{rest}"/></EntryState>'
                  f'<AnimationState x="0" y="130" animationId="{REST}" {"random=\"true\" " if len(TAP[n]) > 1 else ""}id="{rest}">{outs}</AnimationState>'
                  + ''.join(sts) + '</StateMachineLayer>')
    listeners.append(f'<StateMachineListenerSingle targetId="{ids[n + "_body"]}" listenerTypeValue="down" name="tap {n}"><ListenerTriggerChange inputId="{trig}"/></StateMachineListenerSingle>')
sm = (f'<StateMachine name="Home cast" id="0:9002">' + ''.join(inputs) + ''.join(listeners) + ''.join(layers) + '</StateMachine>')
extra = sm + '\n' + '\n'.join(x for _, _, x in anims)
rml = rml.replace('    </Artboard>\n</Rive>', extra + '\n    </Artboard>\n</Rive>')
open(os.path.join(HERE, '../scene.rml'), 'w').write(rml)
print('nodes', len(ids), 'animations', len(anims))
