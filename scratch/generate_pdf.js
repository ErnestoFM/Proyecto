const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const htmlFile = path.resolve('scratch', 'diagrama_recursos.html');
const pdfFile = path.resolve('Actividad_1.7_Diagrama_de_Recursos_Monchis_Cafe.pdf');
const downloadPdf = path.resolve('C:\\Users\\hatue\\Downloads', 'Actividad_1.7_Diagrama_de_Recursos_Monchis_Cafe.pdf');
const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

const htmlUrl = 'file:///' + htmlFile.replace(/\\/g, '/');

console.log('Rendering HTML to PDF...');
const cmd = `"${edgePath}" --headless=new --disable-gpu --no-pdf-header-footer "--print-to-pdf=${pdfFile}" "${htmlUrl}"`;
execSync(cmd, { stdio: 'inherit' });

if (fs.existsSync(pdfFile)) {
    const stats = fs.statSync(pdfFile);
    console.log(`PDF created successfully: ${pdfFile} (${stats.size} bytes)`);
    fs.copyFileSync(pdfFile, downloadPdf);
    console.log(`Copied to Downloads: ${downloadPdf}`);
} else {
    console.error('Failed to create PDF');
    process.exit(1);
}
