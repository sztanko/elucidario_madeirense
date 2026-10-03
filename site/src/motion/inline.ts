// The only synchronous motion code (owner: motion agent). Rendered inline by Plane.astro.
// It must run before the new document's first render to catch `pagereveal`, so it is a tiny
// classic script (~1.1 KB). Everything else is lazy (boot.ts → engine.ts).
//
// The engine module (public/plane/m/fly-*.js, URL in C.e) is imported right here, so the flight
// does not wait for the rest of the document to parse or for deferred module scripts.
//
// window.__emFlight: a promise that settles when the flight is over. Heavy start-up work that is
// invisible during the flight anyway (e.g. the map engine) can wait for it.
//
// Old page, `pageswap`: remember where we take off from (block index, headword, Orientar camera).
// New page, `pagereveal`: if a cross-document view transition is running and both ends sit on the
// plane, choose the mode (fly | card), add the capture layer #em-fly (view-transition-name: em-plane)
// and hand the transition to the engine. If the engine is not running 350 ms after the new
// page was captured (vt.ready), the transition falls back to a 180 ms cross-fade (html.em-late). Navigation itself is never delayed.

export interface InlineCfg { i: number; l: string; v: string; b: string; s: string; e: string; o: string }

export function inlineScript(c: InlineCfg): string {
  return `(function(){var C=window.__em=${JSON.stringify(c)},d=document.documentElement,K='em-from',S;try{S=sessionStorage}catch(x){return}
function rm(){return matchMedia('(prefers-reduced-motion: reduce)').matches}
function hw(){return document.title.split(' — ')[0]}
addEventListener('pageswap',function(e){var v=e.viewTransition;if(!v)return;if(rm()){v.skipTransition();return}
try{var a=e.activation,u=a&&a.entry&&a.entry.url;S.setItem(K,JSON.stringify({i:C.i,t:Date.now(),to:u||'',hw:hw(),cam:window.__emCam||null,w:innerWidth,h:innerHeight}))}catch(x){}});
addEventListener('pagereveal',function(e){var vt=e.viewTransition;if(!vt)return;if(rm()){vt.skipTransition();return}
var f=null;try{f=JSON.parse(S.getItem(K));S.removeItem(K)}catch(x){}
var h=location.href.split('#')[0];if(!f||C.i<0||f.i===C.i||Date.now()-f.t>1e4||(f.to&&f.to.split('#')[0]!==h))return;
var n=navigator,c=n.connection,lite=(c&&c.saveData)||n.deviceMemory<=2||n.hardwareConcurrency<=2||localStorage.getItem('em-motion')==='lite';
var m=lite?'card':'fly',el=document.createElement('div');el.id='em-fly';el.setAttribute('aria-hidden','true');
if(lite){var s=document.createElement('span');s.textContent=hw();el.appendChild(s)}else el.appendChild(document.createElement('canvas'));
d.appendChild(el);d.classList.add('em-'+m);window.__emFlight=vt.finished.catch(function(){});var F=window.__emFly={vt:vt,f:f,m:m,el:el,go:0,t0:performance.now()};
if(!lite){var late=function(){if(!F.go){F.go=-1;d.classList.replace('em-fly','em-late')}};vt.ready.then(function(){setTimeout(late,350)},late);setTimeout(late,2500);import(C.e).then(function(m){m.fly(F)},function(){F.go||vt.skipTransition()})}
vt.finished.finally(function(){C.last=F.go;d.classList.remove('em-'+m,'em-late');el.remove();if(window.__emFly===F)window.__emFly=null})})})();`;
}
