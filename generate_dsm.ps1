param(
  [Parameter(Mandatory=$true)] [string]$UdbPath,
  [Parameter(Mandatory=$true)] [string]$SrcDir,
  [Parameter(Mandatory=$true)] [string]$OutDsm
)

$und = "C:\Program Files\SciTools\bin\pc-win64\und.exe"

Write-Host "1) Creating/opening Understand DB → $UdbPath"
& $und create -db $UdbPath -languages java

Write-Host "2) Adding source files from $SrcDir"
& $und -db $UdbPath add $SrcDir

Write-Host "3) Analyzing…"
& $und analyze $UdbPath

Write-Host "4) Exporting DSM (matrix format) → $OutDsm"
& $und export -dependencies file matrix $OutDsm $UdbPath

Write-Host "✅ Done! Your DSM is at $OutDsm"