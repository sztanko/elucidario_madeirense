// Horizontal scrollers ([data-hscroll]): prev/next arrow buttons, edge fades where more content exists, and a pulsing
// "swipe" cue on the next arrow until the reader has scrolled any row once (remembered in localStorage).
// Works for any element that scrolls on x: timeline card rows, the article folio view, etc. Controls only appear
// while the element actually overflows (ResizeObserver), so the folio body gets them only in folio mode.

const SEEN = 'em:hscroll-seen';
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

function label(dir: 'prev' | 'next'): string {
  const lang = document.documentElement.lang.slice(0, 2);
  const L: Record<string, [string, string, string]> = {
    pt: ['Anterior', 'Seguinte', 'Deslize'], uk: ['Назад', 'Далі', 'Гортайте'], hu: ['Előző', 'Következő', 'Lapozás'],
  };
  const [p, n] = L[lang] ?? ['Previous', 'Next', 'Swipe'];
  return dir === 'prev' ? p : n;
}
function swipeWord(): string {
  const lang = document.documentElement.lang.slice(0, 2);
  return ({ pt: 'Deslize', uk: 'Гортайте', hu: 'Lapozás' } as Record<string, string>)[lang] ?? 'Swipe';
}

function enhance(sc: HTMLElement) {
  if (sc.dataset.hsReady) return;
  sc.dataset.hsReady = '1';
  const wrap = document.createElement('div');
  wrap.className = 'em-hs';
  sc.parentNode!.insertBefore(wrap, sc);
  wrap.appendChild(sc);
  // Controls sit in a bar under the row, never over the text.
  const bar = document.createElement('div');
  bar.className = 'em-hs__bar';
  wrap.appendChild(bar);
  const mk = (dir: 'prev' | 'next') => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = `em-hs__btn em-hs__btn--${dir}`;
    b.setAttribute('aria-label', label(dir));
    b.innerHTML = dir === 'prev' ? '<span aria-hidden="true">←</span>' : '<span aria-hidden="true">→</span>';
    b.addEventListener('click', () => {
      const step = Math.max(sc.clientWidth * 0.85, 160);
      sc.scrollBy({ left: dir === 'prev' ? -step : step, behavior: reduce ? 'auto' : 'smooth' });
    });
    bar.appendChild(b);
    return b;
  };
  const cue = document.createElement('span');
  cue.className = 'em-hs__cue';
  cue.setAttribute('aria-hidden', 'true');
  cue.textContent = swipeWord();
  bar.appendChild(cue);
  mk('prev');
  const next = mk('next');
  if (!localStorage.getItem(SEEN)) wrap.classList.add('is-cue');

  const update = () => {
    const over = sc.scrollWidth > sc.clientWidth + 4;
    wrap.classList.toggle('is-overflow', over);
    wrap.classList.toggle('at-start', sc.scrollLeft <= 4);
    wrap.classList.toggle('at-end', sc.scrollLeft + sc.clientWidth >= sc.scrollWidth - 4);
  };
  let raf = 0;
  sc.addEventListener('scroll', () => {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(update);
    if (sc.scrollLeft > 20 && wrap.classList.contains('is-cue')) {
      localStorage.setItem(SEEN, '1');
      document.querySelectorAll('.em-hs.is-cue').forEach((w) => w.classList.remove('is-cue'));
    }
  }, { passive: true });
  new ResizeObserver(update).observe(sc);
  update();
  void next;
}

export function initHScroll(root: ParentNode = document) {
  root.querySelectorAll<HTMLElement>('[data-hscroll]').forEach(enhance);
}

initHScroll();
