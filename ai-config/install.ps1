[CmdletBinding()]
param(
    [string]$ClaudeDir = (Join-Path $HOME '.claude'),
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot

function Get-InstallPlan {
    $plan = @(@{ Source = Join-Path $PSScriptRoot 'CLAUDE.md'; Target = Join-Path $ClaudeDir 'CLAUDE.md' })
    Get-ChildItem (Join-Path $repoRoot '.claude/agents') -Filter '*.md' | ForEach-Object {
        $plan += @{ Source = $_.FullName; Target = Join-Path $ClaudeDir "agents/$($_.Name)" }
    }
    return $plan
}

function Install-File {
    param([string]$Source, [string]$Target)

    if (-not (Test-Path $Target)) {
        New-Item -ItemType Directory -Force (Split-Path -Parent $Target) | Out-Null
        Copy-Item $Source $Target
        return 'installed'
    }
    if ((Get-FileHash $Source).Hash -eq (Get-FileHash $Target).Hash) { return 'unchanged' }
    if (-not $Force) { return 'skipped (differs, use -Force)' }

    Copy-Item $Target "$Target.bak-$(Get-Date -Format yyyyMMddHHmmss)"
    Copy-Item $Source $Target -Force
    return 'replaced (backup kept)'
}

foreach ($item in Get-InstallPlan) {
    '{0,-28} {1}' -f (Split-Path -Leaf $item.Target), (Install-File $item.Source $item.Target)
}
Write-Host "Merge ai-config/settings.snippet.json into $ClaudeDir/settings.json by hand."
