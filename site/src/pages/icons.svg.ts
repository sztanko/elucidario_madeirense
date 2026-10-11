// Static icon sprite (/icons.svg) referenced by <Icon> via <use href="/icons.svg?v=…#name">.
import type { APIRoute } from 'astro';
import { iconSprite } from '../components/ui/icons-data';

export const GET: APIRoute = () => new Response(iconSprite(), { headers: { 'Content-Type': 'image/svg+xml' } });
