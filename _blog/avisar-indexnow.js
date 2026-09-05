/* ==========================================================================
   AVISAR A BING DE QUE HA CAMBIADO LA WEB  ·  IndexNow
   --------------------------------------------------------------------------
   Publicar la clave en la raíz de la web NO avisa a nadie: eso solo demuestra
   que la web es tuya. El aviso hay que MANDARLO, y es lo que hace esto.

   Sin él, Bing tarda semanas en enterarse de un artículo nuevo. Con él, horas.
   Y como aquí se publican diez artículos por semana, la diferencia se nota.

   CÓMO SE USA
     node _blog/avisar-indexnow.js                 lo que cambió hoy
     node _blog/avisar-indexnow.js --todo          la web entera
     node _blog/avisar-indexnow.js <url> <url>…    esas direcciones y nada más
     node _blog/avisar-indexnow.js --esperar       espera a que estén en línea
     node _blog/avisar-indexnow.js --probar        no manda nada, solo lo cuenta

   SE EJECUTA DESPUÉS DE SUBIR, NO ANTES. Si se avisa de una página que
   todavía no está publicada, Bing va a mirarla, no la encuentra, y se ha
   gastado el aviso. Con --esperar el propio programa comprueba que están en
   línea antes de mandar nada, que es lo cómodo cuando publica GitHub Pages y
   tarda un minuto en reconstruir.

   POR QUÉ EN NODE Y NO EN PYTHON, como el resto del blog: en el PC de Pedro
   el antivirus rompe la verificación de certificados de Python
   ("CERTIFICATE_VERIFY_FAILED: Basic Constraints of CA cert not marked
   critical") y NINGUNA petición https le funciona. Node sí. No lo pases a
   Python "por coherencia": deja de funcionar en su máquina.
   ========================================================================== */

"use strict";

const fs = require("node:fs");
const path = require("node:path");

/* La clave está publicada en la raíz de la web a propósito: así es como
   IndexNow comprueba que el sitio es nuestro. No es un secreto. */
const CLAVE = "a70a4940c8a7423797b1a77a84ce7728";
const HOST  = "www.tpcmetal.es";
const RAIZ  = path.join(__dirname, "..");

const CLAVE_URL = "https://" + HOST + "/" + CLAVE + ".txt";
const ENDPOINT  = "https://api.indexnow.org/indexnow";

const args    = process.argv.slice(2);
const opcion  = o => args.includes(o);
const TODO    = opcion("--todo");
const ESPERAR = opcion("--esperar");
const PROBAR  = opcion("--probar");
const sueltas = args.filter(a => a.startsWith("http"));

const hoy = new Date().toISOString().slice(0, 10);

/** Las direcciones del sitemap, con su fecha de última modificación. */
function delSitemap(){
  const f = path.join(RAIZ, "sitemap.xml");
  if(!fs.existsSync(f)) throw new Error("no encuentro sitemap.xml en " + RAIZ);
  const xml = fs.readFileSync(f, "utf8");
  const urls = [];
  const re = /<url>([\s\S]*?)<\/url>/g;
  let m;
  while((m = re.exec(xml)) !== null){
    const loc = (/<loc>([^<]+)<\/loc>/.exec(m[1]) || [])[1];
    const mod = (/<lastmod>([^<]+)<\/lastmod>/.exec(m[1]) || [])[1] || "";
    if(loc) urls.push({ loc: loc.trim(), mod: mod.trim().slice(0, 10) });
  }
  return urls;
}

/** ¿Está esa dirección publicada ya? */
async function enLinea(url){
  try{
    const r = await fetch(url, { method: "GET", redirect: "follow" });
    return r.status;
  }catch(e){ return 0; }
}

const esperar = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  /* ---- Qué direcciones se avisan ---- */
  let urls;
  if(sueltas.length){
    urls = sueltas;
    console.log("Aviso de las " + urls.length + " direcciones que me has dado.");
  }else{
    const todas = delSitemap();
    if(TODO){
      urls = todas.map(u => u.loc);
      console.log("Aviso de la web entera: " + urls.length + " direcciones del sitemap.");
    }else{
      urls = todas.filter(u => u.mod === hoy).map(u => u.loc);
      console.log("Aviso de lo que cambió hoy (" + hoy + "): " + urls.length +
                  " de las " + todas.length + " del sitemap.");
      if(!urls.length){
        console.log("\nNo hay nada con fecha de hoy en el sitemap. Si acabas de");
        console.log("publicar, comprueba que pasaste _blog/generar.py antes.");
        console.log("Para avisar de todo de golpe: --todo");
        process.exit(0);
      }
    }
  }

  /* Que no se cuele una dirección de otro dominio: IndexNow devuelve 422 y
     no dice cuál era. */
  const ajenas = urls.filter(u => { try{ return new URL(u).host !== HOST; }catch(e){ return true; } });
  if(ajenas.length){
    console.error("\nEstas direcciones NO son de " + HOST + " y sobran:");
    ajenas.forEach(u => console.error("   " + u));
    process.exit(1);
  }

  urls.forEach(u => console.log("   " + u));

  /* ---- La clave tiene que estar publicada ---- */
  const cod = await enLinea(CLAVE_URL);
  if(cod !== 200){
    console.error("\nLa clave NO está publicada: " + CLAVE_URL + " responde " + cod + ".");
    console.error("Sin eso Bing rechaza el aviso (403). Sube el fichero");
    console.error("'" + CLAVE + ".txt' a la raíz de la web y vuelve a intentarlo.");
    process.exit(1);
  }
  console.log("\nLa clave está publicada y responde bien.");

  /* ---- Esperar a que las páginas estén en línea ---- */
  if(ESPERAR){
    console.log("\nEsperando a que las páginas estén publicadas…");
    for(let intento = 1; intento <= 20; intento++){
      const codigos = await Promise.all(urls.map(enLinea));
      const faltan = urls.filter((u, i) => codigos[i] !== 200);
      if(!faltan.length){ console.log("   todas en línea."); break; }
      if(intento === 20){
        console.error("   siguen sin publicarse: " + faltan.join(", "));
        console.error("   No aviso: sería gastar el aviso para nada.");
        process.exit(1);
      }
      console.log("   faltan " + faltan.length + ", reintento en 15 s (" + intento + "/20)");
      await esperar(15000);
    }
  }

  if(PROBAR){
    console.log("\n--probar: no se ha mandado nada.");
    process.exit(0);
  }

  /* ---- El aviso ---- */
  const cuerpo = JSON.stringify({
    host: HOST,
    key: CLAVE,
    keyLocation: CLAVE_URL,
    urlList: urls
  });

  const r = await fetch(ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: cuerpo
  });

  /* IndexNow contesta con el código y poco más; se traduce a román paladino. */
  const QUE_SIGNIFICA = {
    200: "Recibido. Bing ya sabe que estas páginas han cambiado.",
    202: "Recibido. Está comprobando la clave; es normal las primeras veces.",
    400: "Formato incorrecto: revisa las direcciones.",
    403: "Rechaza la clave. Comprueba que el fichero de la raíz sigue publicado.",
    422: "Las direcciones no cuadran con el dominio, o la clave no es la de esta web.",
    429: "Demasiados avisos seguidos. Espera un rato y no avises de todo a cada rato."
  };
  const texto = await r.text().catch(() => "");
  console.log("\nRespuesta de IndexNow: " + r.status +
              (QUE_SIGNIFICA[r.status] ? "  ·  " + QUE_SIGNIFICA[r.status] : ""));
  if(texto.trim()) console.log("   " + texto.trim().slice(0, 200));

  const bien = r.status === 200 || r.status === 202;
  if(!bien) console.error("\nEl aviso NO ha entrado.");
  process.exit(bien ? 0 : 1);
})().catch(e => {
  console.error("Error: " + (e && e.message ? e.message : e));
  process.exit(1);
});
