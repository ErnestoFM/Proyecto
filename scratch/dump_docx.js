const fs = require('fs');
const { execSync } = require('child_process');
const path = require('path');

function readDocx(filename) {
    const tmp = path.join(__dirname, 'temp_docx_' + Math.random().toString(36).substring(7));
    if (!fs.existsSync(tmp)) fs.mkdirSync(tmp, { recursive: true });
    const fullPath = path.resolve(filename);
    const tempZip = path.join(tmp, 'doc.zip');
    fs.copyFileSync(fullPath, tempZip);
    execSync(`powershell -NoProfile -Command "Expand-Archive -LiteralPath '${tempZip}' -DestinationPath '${tmp}' -Force"`);
    const xml = fs.readFileSync(path.join(tmp, 'word', 'document.xml'), 'utf8');
    const text = xml.replace(/<w:p[^>]*>/g, '\n').replace(/<[^>]+>/g, '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
    fs.rmSync(tmp, { recursive: true, force: true });
    return text;
}

const txt = readDocx('Actividad_1.3_Presupuesto_Monchis_Cafe.docx');
fs.writeFileSync(path.join(__dirname, 'presupuesto_extraido.txt'), txt, 'utf8');
console.log('Saved presupuesto_extraido.txt, length:', txt.length);

const txtRoles = readDocx('Actividad_Definicion_de_Roles_Monchis_Cafe.docx');
fs.writeFileSync(path.join(__dirname, 'roles_extraido.txt'), txtRoles, 'utf8');
console.log('Saved roles_extraido.txt, length:', txtRoles.length);
