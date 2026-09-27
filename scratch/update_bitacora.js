const fs = require('fs');
let content = fs.readFileSync('obsidian/Bitacora/2026-09-26.md', 'utf8');
content = content.replace(
  'Viernes 02 de Octubre de 2026 (calculado con WORKDAY(..., ROUNDUP(Te,0)-1) asegurando los 35 días hábiles exactos sin pérdida por truncamiento decimal).',
  'Viernes 02 de Octubre de 2026 (anclado robustamente al EF acumulado en días mediante WORKDAY($R$10, ROUND(M_row, 0) - 1), eliminando distorsiones por redondeos independientes y sincronizando el día dinámico con PROPER(TEXT(..., "dddd"))).'
);
fs.writeFileSync('obsidian/Bitacora/2026-09-26.md', content, 'utf8');
console.log('Bitacora updated successfully');
