python.exe -m venv .venv_win

.venv_win\Scripts\python.exe -m pip install --upgrade pip
.venv_win\Scripts\pip.exe install -r requirements.txt

.venv_win\Scripts\python.exe -m pytest

$file = "../pyinstaller-5.8.0.zip"
if (-not(Test-Path -Path $file -PathType Leaf)) {
    try {
        $client = new-object System.Net.WebClient
        $client.DownloadFile("https://github.com/pyinstaller/pyinstaller/archive/refs/tags/v5.8.0.zip", $file)
    }
    catch {
        throw $_.Exception.Message
    }
}

$folder = "../pyinstaller-5.8.0/"
if (-not(Test-Path -Path $folder)) {
    try {
        Expand-Archive -Path $file -DestinationPath "../"
    }
    catch {
        throw $_.Exception.Message
    }
}

Set-Location ..\pyinstaller-5.8.0\bootloader\
..\..\sbfrm\.venv_win\Scripts\python.exe ./waf all --target-arch=64bit
Set-Location ..\
..\sbfrm\.venv_win\Scripts\pip.exe install .
Set-Location ..\sbfrm\