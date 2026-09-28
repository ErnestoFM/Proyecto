const fs = require('fs');
const { execSync } = require('child_process');
const path = require('path');

function readDocx(filename) {
    const tmp = path.join(__dirname, 'temp_docx_' + Date.now());
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

try {
    console.log('=== PRESUPUESTO ===');
    console.log(readDocx('Actividad_1.3_Presupuesto_Monchis_Cafe.docx'));
} catch (e) {
    console.error('Error presupuesto:', e.message);
}

try {
    console.log('=== ROLES ===');
    console.log(readDocx('Actividad_Definicion_de_Roles_Monchis_Cafe.docx'));
} catch (e) {
    console.error('Error roles:', e.message);
}
