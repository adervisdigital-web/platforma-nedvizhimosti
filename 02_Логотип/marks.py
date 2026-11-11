"""Logo marks for the three variants (light / dark / bright). All built on the letter П."""



def mark_D(w, front='#F2F1EE', top='#A7ACB4', side='#5C616B', glow='#FFB547', label='Знак «Портал»', mono=None):
    # П extruded in axonometry; warm light on the inner wall of the doorway
    if mono:
        front = top = side = glow = mono
    h = round(w * 36 / 36, 2)
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 36 36" role="img" aria-label="{label}">'
            f'<polygon points="0,8 8,0 36,0 28,8" fill="{top}"/>'
            f'<polygon points="28,8 36,0 36,28 28,36" fill="{side}"/>'
            f'<polygon points="8,16 16,16 16,28 8,36" fill="{glow}"/>'
            f'<path d="M0 8 H28 V36 H20 V16 H8 V36 H0 Z" fill="{front}"/></svg>')


def mark_Y(w, c1='#2E4BFF', c2='#FF6B2C', c3='#18B26B', label='Знак «Сборка»'):
    # П assembled from three mitred parts: квартиры (left), ремонт (top), дома (right)
    h = round(w * 36 / 40, 2)
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 40 36" role="img" aria-label="{label}">'
            f'<polygon points="0,0 40,0 30,10 10,10" fill="{c2}"/>'
            f'<polygon points="0,3 10,13 10,36 0,36" fill="{c1}"/>'
            f'<polygon points="40,3 40,36 30,36 30,13" fill="{c3}"/></svg>')
def mark_L(w, ink='#B4532A', acc=None, label='Знак «Арка»'):
    # square block with an arched doorway: the letter П and an entrance to a stone house
    h = round(w * 40 / 36, 2)
    d = 'M0 0 H36 V40 H26 V20 A8 8 0 0 0 10 20 V40 H0 Z'
    extra = f'<rect x="10" y="34" width="16" height="6" fill="{acc}"/>' if acc else ''
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 36 40" role="img" aria-label="{label}">'
            f'<path d="{d}" fill="{ink}"/>{extra}</svg>')
