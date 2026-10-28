$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$wb = $excel.Workbooks.Open("d:\ernestofm\Proyecto\docs\entregables\Actividad_4_Gestion_Finanzas_MonchisCafe.xlsx")
$ws = $wb.Sheets.Item("RESUMEN Y COTIZACION")
for ($r = 1; $r -le 26; $r++) {
    $a = $ws.Cells.Item($r, 1).Text
    $b = $ws.Cells.Item($r, 2).Text
    if ($a -or $b) {
        Write-Output ("R{0:D2}: {1,-40} = {2}" -f $r, $a, $b)
    }
}
$wb.Close($false)
$excel.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
