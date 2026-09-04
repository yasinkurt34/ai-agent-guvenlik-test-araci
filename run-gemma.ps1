param([int]$Repeats = 1, [switch]$ListModels)
# The model imported from the user's Desktop into LM Studio.
& (Join-Path $PSScriptRoot 'run-lmstudio.ps1') -Model 'gemma-4-e4b-it' -Repeats $Repeats -ListModels:$ListModels
exit $LASTEXITCODE
