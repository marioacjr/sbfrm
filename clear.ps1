$FolderName = ".\.venv_win\"
if (Test-Path $FolderName) {
    Remove-Item -LiteralPath $FolderName -Force -Recurse
}

$FolderName = ".\.pytest_cache\"
if (Test-Path $FolderName) {
    Remove-Item -LiteralPath $FolderName -Force -Recurse
}

$FolderName = ".\__pytest_cache__\"
if (Test-Path $FolderName) {
    Remove-Item -LiteralPath $FolderName -Force -Recurse
}

$FolderName = ".\build\"
if (Test-Path $FolderName) {
    Remove-Item -LiteralPath $FolderName -Force -Recurse
}

$FolderName = ".\dist\"
if (Test-Path $FolderName) {
    Remove-Item -LiteralPath $FolderName -Force -Recurse
}