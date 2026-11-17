# Reglas de este sitio (gensat-digital.github.io)

Web de GENSAT LLC, publicada con GitHub Pages desde la rama `main`. Todo lo que entra a `main` queda público en minutos.

## Reglas fijas
- **No cambiar el logo de GENSAT** (el símbolo SVG de la "G" con barras y el texto "ENSAT"). Las mejoras de diseño van en portada, fondos, animaciones y tarjetas, nunca en el logo.
- Bilingüe: todo texto nuevo se agrega en español **y** en inglés (objeto `T` en `index.html`).
- Debe verse y funcionar en teléfono (390 px) y en computadora (1366 px), sin desplazamiento horizontal.
- Precios siempre en dólares (USD).
- Contacto oficial: WhatsApp +1 (385) 574-5556 · Instagram @yeison_e_genes_v. Nunca usar @gensat10 como usuario de redes.
- Nada de café en textos, imágenes ni demos. Nunca mencionar Nutrix ni datos reales de empresas: los demos usan datos de ejemplo.
- Las carpetas `clientes/` son páginas privadas de clientes: no enlazarlas desde la portada ni mezclar datos de un cliente en otro.
- Trabajar en una rama nueva y abrir un pull request; **publicar (merge a `main`) solo con la orden de Yeison**.

## Antes de publicar (lista de revisión, debe pasar todo)
1. Probar con Playwright en 390x844 y 1366x800: sin errores de consola y `scrollWidth` igual al ancho.
2. Revisar con las reglas de interfaz de Vercel (github.com/vercel-labs/web-interface-guidelines): foco visible y uso con teclado, íconos decorativos con `aria-hidden`, imágenes con `width`/`height`, `prefers-reduced-motion` respetado, animaciones que no se repiten sin fin, botones de al menos 44 px en el teléfono, sin `transition: all`.
3. Confirmar que el logo quedó idéntico.
4. Español e inglés completos.
