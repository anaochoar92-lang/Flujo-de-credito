# Crea 12-roi/Modelo_ROI_Flujo_Credito.xlsx con fórmulas vivas (requiere Excel instalado).
# Uso: powershell -File trabajos/mi-proceso/12-roi/crear_excel_roi.ps1
# Entrada: 12-roi/conteos_mensuales.csv (node trabajos/mi-proceso/12-roi/conteos.js)
$ErrorActionPreference = 'Stop'
$dir = $PSScriptRoot
$salida = Join-Path $dir 'Modelo_ROI_Flujo_Credito.xlsx'
$conteos = Import-Csv (Join-Path $dir 'conteos_mensuales.csv')

$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
$wb = $xl.Workbooks.Add()
while ($wb.Worksheets.Count -lt 6) { [void]$wb.Worksheets.Add([Type]::Missing, $wb.Worksheets.Item($wb.Worksheets.Count)) }
$hojas = 'LEEME', 'Opciones', 'ROI', 'Supuestos', 'Conteos', 'FlujoMensual'
for ($i = 0; $i -lt 6; $i++) { $wb.Worksheets.Item($i + 1).Name = $hojas[$i] }
$wsL = $wb.Worksheets.Item('LEEME'); $wsS = $wb.Worksheets.Item('Supuestos'); $wsC = $wb.Worksheets.Item('Conteos')
$wsR = $wb.Worksheets.Item('ROI'); $wsF = $wb.Worksheets.Item('FlujoMensual'); $wsO = $wb.Worksheets.Item('Opciones')
function Fila($ws, $r, $vals) { for ($k = 0; $k -lt $vals.Count; $k++) { if ($null -ne $vals[$k]) { $ws.Cells.Item($r, $k + 1).Formula = [string]$vals[$k] } } }
function Titulo($ws, $texto) { $ws.Cells.Item(1, 1).Value2 = $texto; $ws.Cells.Item(1, 1).Font.Bold = $true; $ws.Cells.Item(1, 1).Font.Size = 14 }
function Encabezado($ws, $r, $vals) { Fila $ws $r $vals; $ws.Range($ws.Cells.Item($r, 1), $ws.Cells.Item($r, $vals.Count)).Font.Bold = $true
  $ws.Range($ws.Cells.Item($r, 1), $ws.Cells.Item($r, $vals.Count)).Interior.Color = 0xEADBC8 }
# Formatos con los separadores del Excel instalado (en español: coma decimal y punto de miles)
$ds = $xl.International(3); $ts = $xl.International(4)
$RD = """RD$"" #$ts##0"; $PCT = "0$($ds)0%"; $NUM = "#$ts##0"; $DEC = "#$ts##0$($ds)00"; $RD2 = """RD$"" #$ts##0$($ds)00"; $UNO = "0$($ds)0"

# --- LEEME -------------------------------------------------------------------
Titulo $wsL 'Modelo de ROI - Flujo de crédito preaprobado Expomóvil (SINTÉTICO)'
$notas = @(
  'Datos SINTÉTICOS (09-datos, semilla 20261024). Un ROI sintético NO valida una inversión.',
  'Moneda: pesos dominicanos (RD$). Celdas amarillas de la hoja Supuestos = editables.',
  'MODELO ADOPTADO = Opción 3 (ronda 12): versión mínima del portal sobre Camunda, mensajero de un tercero cobrado al cliente como comisión (sin costo para el banco) y el tiempo liberado fuera de feria se convierte en caja (no reponer puestos).',
  'Hoja Opciones: compara el modelo original con las opciones 1, 2 y 3 (escenario base). Hojas ROI y FlujoMensual: modelo adoptado.',
  'Caja = menos personal temporal en feria (ROI-4) + tiempo liberado convertido en caja (% editable en Supuestos, fila 24).',
  'ROI año 1 = (beneficio en caja - opex - inversión) / (opex + inversión). Opex = mensajero (si aplica) + mantenimiento.',
  'Beneficio NO incluido: créditos que dejan de perderse por vencimiento (ver ROI, fila 28). Falta el margen por crédito.',
  'Regenerar: node trabajos/mi-proceso/12-roi/conteos.js y luego este script (crear_excel_roi.ps1).')
for ($k = 0; $k -lt $notas.Count; $k++) { $wsL.Cells.Item($k + 3, 1).Value2 = $notas[$k] }
$wsL.Columns.Item(1).ColumnWidth = 120

# --- Supuestos ---------------------------------------------------------------
Titulo $wsS 'Supuestos (editar celdas amarillas)'
Encabezado $wsS 3 @('Variable', 'Unidad', 'Conservador', 'Base', 'Optimista', 'Estado / fuente')
$sup = @(
  @(4, 'Salario mínimo mensual (empresa grande)', 'RD$/mes', 29988, 29988, 29988, 'Declarado (ROI-1). Res. CNS-01-2025, vigente desde 01-02-2026'),
  @(5, 'Factor de costo del empleador', 'x', 1.25, 1.25, 1.25, 'SUPUESTO S-1: TSS empleador ~16 % + regalía pascual 8,3 %'),
  @(6, 'Días laborables por mes', 'días', 23.83, 23.83, 23.83, 'Práctica laboral RD'),
  @(7, 'Horas por día', 'h', 8, 8, 8, 'Declarado (ROI-2)'),
  @(11, 'ACT_006 Recopilar expediente (Legal)', 'h/ejecución', 0.75, 1.5, 2.25, 'HIPÓTESIS H-R1: horas de trabajo real por expediente'),
  @(12, 'ACT_007 Escanear documentación (Legal)', 'h/ejecución', 0.5, 1, 1.5, 'HIPÓTESIS H-R1'),
  @(13, 'ACT_008 Verificar expediente en papel (Despacho)', 'h/ejecución', 0.5, 1, 1.5, 'HIPÓTESIS H-R1'),
  @(14, 'TB_ACT_VERIF Verificar expediente digital (Despacho)', 'h/ejecución', 0.25, 0.5, 0.75, 'HIPÓTESIS H-R1'),
  @(15, 'TB_ACT_PEDIR Pedir documento corregido (Despacho)', 'h/ejecución', 0.125, 0.25, 0.375, 'HIPÓTESIS H-R1'),
  @(16, 'TB_ACT_RECOP_ORIG Recopilar originales (Legal)', 'h/ejecución', 0.5, 1, 1.5, 'HIPÓTESIS H-R1'),
  @(17, 'TB_ACT_ESCANEAR Escanear originales (Legal)', 'h/ejecución', 0.5, 1, 1.5, 'HIPÓTESIS H-R1'),
  @(19, 'Costo por recogida del mensajero certificado', 'RD$/recogida', 500, 400, 300, 'SUPUESTO S-2 (lo paga el banco solo si fila 23 = 1)'),
  @(20, 'Inversión inicial: versión mínima del portal sobre Camunda', 'RD$', 1500000, 1000000, 700000, 'SUPUESTO S-3b (Opción 3, ronda 12)'),
  @(21, 'Mantenimiento anual (% de la inversión)', '%', 0.20, 0.15, 0.10, 'SUPUESTO S-4b (Opción 3)'),
  @(23, '¿El banco paga el mensajero? (1 = sí, 0 = tercero cobrado al cliente como comisión)', '1/0', 0, 0, 0, 'Decisión Opción 1 (ronda 13, ROI-7)'),
  @(24, '% del tiempo liberado fuera de feria que se convierte en caja', '%', 0.5, 1, 1, 'Decisión Opción 2 (ronda 12): no reponer puestos; SUPUESTO S-5 en conservador'))
foreach ($q in $sup) { Fila $wsS $q[0] @($q[1], $q[2], $q[3], $q[4], $q[5], $q[6]); $wsS.Range("C$($q[0]):E$($q[0])").Interior.Color = 0x99FFFF }
$wsS.Cells.Item(10, 1).Value2 = 'Horas de trabajo por ejecución de cada actividad'; $wsS.Cells.Item(10, 1).Font.Bold = $true
Fila $wsS 8 @('Costo por hora', 'RD$/h', '=C4*C5/(C6*C7)', '=D4*D5/(D6*D7)', '=E4*E5/(E6*E7)', 'Fórmula')
Fila $wsS 22 @('Mantenimiento anual', 'RD$/año', '=C20*C21', '=D20*D21', '=E20*E21', 'Fórmula')
$wsS.Range('C4:E4').NumberFormatLocal = $RD; $wsS.Range('C8:E8').NumberFormatLocal = $RD2; $wsS.Range('C19:E20').NumberFormatLocal = $RD
$wsS.Range('C21:E21').NumberFormatLocal = $PCT; $wsS.Range('C24:E24').NumberFormatLocal = $PCT; $wsS.Range('C22:E22').NumberFormatLocal = $RD

# --- Conteos -------------------------------------------------------------------
Titulo $wsC 'Ejecuciones de actividades por mes y escenario (desde 09-datos, SINTÉTICO)'
$cols = 'mes', 'temporada', 'escenario', 'ACT_006', 'ACT_007', 'ACT_008', 'TB_ACT_VERIF', 'TB_ACT_PEDIR', 'TB_ACT_RECOP_ORIG', 'TB_ACT_ESCANEAR', 'TB_ACT_RECOGER', 'entraron_expediente', 'cerradas_vencimiento', 'sobres_enviados'
Encabezado $wsC 3 $cols
$r = 4
foreach ($row in $conteos) { for ($k = 0; $k -lt $cols.Count; $k++) { $v = $row.($cols[$k]); if ($k -ge 3) { $wsC.Cells.Item($r, $k + 1).Value2 = [double]$v } else { $wsC.Cells.Item($r, $k + 1).Value2 = [string]$v } }; $r++ }
$wsC.Range('A4:A27').NumberFormatLocal = '@'
$rng = { param($col) "Conteos!`$$col`$4:`$$col`$27" }

# --- ROI -------------------------------------------------------------------
Titulo $wsR 'ROI del modelo adoptado (Opción 3): tres escenarios de sensibilidad (año 1)'
Encabezado $wsR 3 @('Concepto', 'Unidad', 'Conservador', 'Base', 'Optimista', 'Cómo se calcula')
function Horas($X, $esc, $temp) {
  $p = @(); $map = @{ D = 11; E = 12; F = 13; G = 14; H = 15; I = 16; J = 17 }
  foreach ($c in 'D', 'E', 'F', 'G', 'H', 'I', 'J') { $p += "$(& $rng $c)*Supuestos!$X`$$($map[$c])" }
  "=SUMPRODUCT(($(& $rng 'C')=""$esc"")*($(& $rng 'B')=""$temp"")*($($p -join '+')))"
}
$filas = @(
  @(5, 'Horas de Legal y Despacho AS-IS, meses de feria', 'h/año', { param($X) Horas $X 'AS-IS' 'feria' }, 'Ejecuciones x horas por ejecución', $NUM),
  @(6, 'Horas de Legal y Despacho TO-BE, meses de feria', 'h/año', { param($X) Horas $X 'TO-BE' 'feria' }, 'Ídem', $NUM),
  @(7, 'Horas ahorradas en feria', 'h/año', { param($X) "=${X}5-${X}6" }, 'AS-IS - TO-BE', $NUM),
  @(8, 'Personal temporal evitado en feria', 'personas-mes', { param($X) "=${X}7/(Supuestos!${X}6*Supuestos!${X}7)" }, 'Horas / (días x horas por persona)', $DEC),
  @(9, 'AHORRO EN CAJA: menos temporales en feria', 'RD$/año', { param($X) "=${X}7*Supuestos!${X}8" }, 'Horas ahorradas en feria x costo hora (ROI-4)', $RD),
  @(11, 'Horas AS-IS, meses sin feria', 'h/año', { param($X) Horas $X 'AS-IS' 'no feria' }, '', $NUM),
  @(12, 'Horas TO-BE, meses sin feria', 'h/año', { param($X) Horas $X 'TO-BE' 'no feria' }, '', $NUM),
  @(13, 'Horas liberadas fuera de feria', 'h/año', { param($X) "=${X}11-${X}12" }, 'Capacidad, no caja', $NUM),
  @(14, 'Valor del tiempo liberado fuera de feria', 'RD$/año', { param($X) "=${X}13*Supuestos!${X}8" }, 'Horas liberadas x costo hora', $RD),
  @(15, 'AHORRO EN CAJA: tiempo liberado convertido (no reponer puestos)', 'RD$/año', { param($X) "=${X}14*Supuestos!${X}24" }, 'Opción 2: valor x % convertido', $RD),
  @(16, 'Recogidas a domicilio', 'recogidas/año', { param($X) "=SUMPRODUCT(($(& $rng 'C')=""TO-BE"")*$(& $rng 'K'))" }, 'TB_ACT_RECOGER (el mensajero se mantiene)', $NUM),
  @(17, 'Costo del mensajero para el banco', 'RD$/año', { param($X) "=${X}16*Supuestos!${X}19*Supuestos!${X}23" }, 'Costo para el banco: 0 si lo paga el cliente como comisión (Opción 1)', $RD),
  @(18, 'Mantenimiento del portal', 'RD$/año', { param($X) "=Supuestos!${X}22" }, '', $RD),
  @(19, 'Opex año 1', 'RD$/año', { param($X) "=${X}17+${X}18" }, 'Mensajero + mantenimiento', $RD),
  @(20, 'Inversión inicial (versión mínima)', 'RD$', { param($X) "=Supuestos!${X}20" }, 'Opción 3', $RD),
  @(21, 'Beneficio total en caja', 'RD$/año', { param($X) "=${X}9+${X}15" }, 'Temporales en feria + tiempo convertido', $RD),
  @(22, 'Beneficio neto operativo anual (caja)', 'RD$/año', { param($X) "=${X}21-${X}19" }, 'Beneficio en caja - opex', $RD),
  @(23, 'ROI año 1 (caja)', '%', { param($X) "=(${X}21-${X}19-${X}20)/(${X}19+${X}20)" }, '(beneficio - opex - inversión) / (opex + inversión)', $PCT),
  @(24, 'Meses de recuperación', 'meses', { param($X) "=IF(${X}22>0,${X}20/(${X}22/12),""No se recupera"")" }, 'Inversión / beneficio neto mensual', $UNO),
  @(26, 'ROI año 1 sin convertir el tiempo liberado en caja (referencia)', '%', { param($X) "=(${X}9-${X}19-${X}20)/(${X}19+${X}20)" }, 'Si no se ejecuta la Opción 2', $PCT),
  @(28, 'NO INCLUIDO: créditos que dejan de perderse por vencimiento', 'créditos/año', { param($X) "=SUMPRODUCT(($(& $rng 'C')=""AS-IS"")*$(& $rng 'M'))-SUMPRODUCT(($(& $rng 'C')=""TO-BE"")*$(& $rng 'M'))" }, 'Falta el margen por crédito para monetizarlo', $NUM))
foreach ($f in $filas) {
  $wsR.Cells.Item($f[0], 1).Value2 = $f[1]; $wsR.Cells.Item($f[0], 2).Value2 = $f[2]; $wsR.Cells.Item($f[0], 6).Value2 = $f[4]
  foreach ($X in 'C', 'D', 'E') { $wsR.Range("$X$($f[0])").Formula = (& $f[3] $X); $wsR.Range("$X$($f[0])").NumberFormatLocal = $f[5] }
}
foreach ($b in 9, 15, 21, 22, 23, 24) { $wsR.Range("A${b}:E${b}").Font.Bold = $true }

# --- FlujoMensual (escenario base) ------------------------------------------------
Titulo $wsF 'Flujo mensual - modelo adoptado (Opción 3), escenario BASE (RD$)'
Encabezado $wsF 3 @('mes', 'temporada', 'Horas AS-IS', 'Horas TO-BE', 'Horas ahorradas', 'Ahorro temporales (feria)', 'Tiempo convertido en caja', 'Mensajero (banco)', 'Mantenimiento', 'Neto en caja', 'Acumulado')
Fila $wsF 4 @('Mes 0', 'inversión', $null, $null, $null, $null, $null, $null, $null, '=-Supuestos!D20', '=J4')
for ($m = 0; $m -lt 12; $m++) {
  $r = 5 + $m; $a = 4 + 2 * $m; $t = $a + 1
  $h = { param($fila) "Conteos!D$fila*Supuestos!`$D`$11+Conteos!E$fila*Supuestos!`$D`$12+Conteos!F$fila*Supuestos!`$D`$13+Conteos!G$fila*Supuestos!`$D`$14+Conteos!H$fila*Supuestos!`$D`$15+Conteos!I$fila*Supuestos!`$D`$16+Conteos!J$fila*Supuestos!`$D`$17" }
  Fila $wsF $r @("=Conteos!A$a", "=Conteos!B$a", "=$(& $h $a)", "=$(& $h $t)", "=C$r-D$r",
    "=IF(B$r=""feria"",E$r*Supuestos!`$D`$8,0)", "=IF(B$r=""no feria"",E$r*Supuestos!`$D`$8*Supuestos!`$D`$24,0)",
    "=Conteos!K$t*Supuestos!`$D`$19*Supuestos!`$D`$23", "=Supuestos!`$D`$22/12", "=F$r+G$r-H$r-I$r", "=K$($r - 1)+J$r")
}
$wsF.Range('C4:E16').NumberFormatLocal = $NUM; $wsF.Range('F4:K16').NumberFormatLocal = $RD

# --- Opciones (escenario base) ----------------------------------------------------
Titulo $wsO 'Opciones para subir el ROI (escenario base, año 1) - ronda 12'
Encabezado $wsO 3 @('Concepto', 'Modelo original', 'Opción 1: mensajero cobrado al cliente', 'Opción 2: + tiempo en caja', 'Opción 3: + versión mínima (ADOPTADA)', 'Nota')
$op = @(
  @(4, 'Inversión inicial (RD$)', 3500000, 3500000, 3500000, '=Supuestos!D20', 'Portal completo vs versión mínima sobre Camunda'),
  @(5, 'Mantenimiento anual (% de la inversión)', 0.2, 0.2, 0.2, '=Supuestos!D21', ''),
  @(6, '¿El banco paga el mensajero? (1/0)', 1, 0, 0, '=Supuestos!D23', 'Opción 1: lo opera un tercero y se cobra al cliente como comisión del servicio'),
  @(7, '% del tiempo liberado que se convierte en caja', 0, 0, 1, '=Supuestos!D24', 'Opción 2: no reponer ~2,7 puestos fuera de feria'))
foreach ($q in $op) { Fila $wsO $q[0] @($q[1], $q[2], $q[3], $q[4], $q[5], $q[6]); $wsO.Range("B$($q[0]):D$($q[0])").Interior.Color = 0x99FFFF }
$calc = @(
  @(9, 'Ahorro temporales en feria', { param($X) '=ROI!$D$9' }, $RD),
  @(10, 'Tiempo liberado convertido en caja', { param($X) "=ROI!`$D`$14*${X}7" }, $RD),
  @(11, 'Beneficio total en caja', { param($X) "=${X}9+${X}10" }, $RD),
  @(12, 'Mensajero (costo para el banco)', { param($X) "=SUMPRODUCT((Conteos!`$C`$4:`$C`$27=""TO-BE"")*Conteos!`$K`$4:`$K`$27)*Supuestos!`$D`$19*${X}6" }, $RD),
  @(13, 'Mantenimiento', { param($X) "=${X}4*${X}5" }, $RD),
  @(14, 'Opex', { param($X) "=${X}12+${X}13" }, $RD),
  @(15, 'Beneficio neto anual (caja)', { param($X) "=${X}11-${X}14" }, $RD),
  @(16, 'ROI año 1 (caja)', { param($X) "=(${X}11-${X}14-${X}4)/(${X}14+${X}4)" }, $PCT),
  @(17, 'Meses de recuperación', { param($X) "=IF(${X}15>0,${X}4/(${X}15/12),""No se recupera"")" }, $UNO))
foreach ($q in $calc) { $wsO.Cells.Item($q[0], 1).Value2 = $q[1]
  foreach ($X in 'B', 'C', 'D', 'E') { $wsO.Range("$X$($q[0])").Formula = (& $q[2] $X); $wsO.Range("$X$($q[0])").NumberFormatLocal = $q[3] } }
$wsO.Range('B4:E4').NumberFormatLocal = $RD; $wsO.Range('B5:E5').NumberFormatLocal = $PCT; $wsO.Range('B7:E7').NumberFormatLocal = $PCT
$wsO.Range('E3:E17').Interior.Color = 0xCCFFCC; foreach ($b in 11, 15, 16, 17) { $wsO.Range("A${b}:E${b}").Font.Bold = $true }
$wsO.Cells.Item(19, 1).Value2 = 'La columna de la Opción 3 toma sus valores de la hoja Supuestos (columna Base). Las columnas B a D son editables.'

foreach ($ws in $wsS, $wsC, $wsR, $wsF, $wsO) { [void]$ws.Columns.AutoFit() }
$wsO.Columns.Item(1).ColumnWidth = 46
$wsR.Columns.Item(1).ColumnWidth = 58; $wsS.Columns.Item(1).ColumnWidth = 50
$xl.CalculateFull()
$wsO.Activate()
if (Test-Path $salida) { Remove-Item $salida -Force }
$wb.SaveAs($salida, 51)
# Resumen en consola
foreach ($f in $filas) { '{0,-62} {1,16} {2,16} {3,16}' -f $f[1], $wsR.Range("C$($f[0])").Text, $wsR.Range("D$($f[0])").Text, $wsR.Range("E$($f[0])").Text }
'Acumulado base al mes 12: ' + $wsF.Range('K16').Text
foreach ($q in $calc) { '{0,-40} {1,18} {2,18} {3,18} {4,18}' -f $q[1], $wsO.Range("B$($q[0])").Text, $wsO.Range("C$($q[0])").Text, $wsO.Range("D$($q[0])").Text, $wsO.Range("E$($q[0])").Text }
$wb.Close($false); $xl.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($xl)
