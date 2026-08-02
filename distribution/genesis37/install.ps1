$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "AletheusOS Genesis 37.21 distribution package"
Write-Host "Manifest: $Root\manifest.json"
Write-Host "This source-first package requires the outer Genesis installer to hydrate it into AletheusOS."
