// Article-length gauge, shared by the server component (LenGauge.astro) and client-rendered lists (search).
// A hairline track that fills on a log scale (80 chars → step 1 … 160,000 chars → step 12); step 0 = no body
// (cross-reference). Tooltip: reading time in the page language (same rate as the article header: 1,150 chars/min).
import { t } from '../../i18n/ui';

const LO = Math.log(80), HI = Math.log(160000);
export const lenStep = (chars: number) =>
  chars <= 0 ? 0 : Math.max(1, Math.min(12, Math.round((12 * (Math.log(chars) - LO)) / (HI - LO))));
export const readMinutes = (chars: number) => Math.max(1, Math.round(chars / 1150));
export const lenTitle = (chars: number, lang: string) => (chars > 0 ? `${readMinutes(chars)} ${t(lang as any, 'min_read')}` : '');
export const gaugeHtml = (chars: number, lang: string) =>
  `<span class="em-len" data-l="${lenStep(chars)}"${chars > 0 ? ` title="${lenTitle(chars, lang)}"` : ''} aria-hidden="true"></span>`;
