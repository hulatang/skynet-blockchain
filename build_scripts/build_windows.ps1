# $env:path should contain a path to editbin.exe and signtool.exe
# Execute this script from project root folder.

# clear dirs
Write-Output "Clear all windows builds"
Write-Output "......"
rm .\build_scripts\build -Recurse -erroraction 'silentlycontinue'
rm .\build_scripts\dist -Recurse -erroraction 'silentlycontinue'
rm .\build_scripts\win_build -Recurse -erroraction 'silentlycontinue'
rm .\venv -Recurse -erroraction 'silentlycontinue'
rm .\skynet-blockchain-gui\build -Recurse -erroraction 'silentlycontinue'
rm .\skynet-blockchain-gui\daemon -Recurse -erroraction 'silentlycontinue'
#rm .\skynet-blockchain-gui\node_modules -Recurse
rm .\skynet-blockchain-gui\release-builds -Recurse -erroraction 'silentlycontinue'
rm .\skynet-blockchain-gui\Skynet-win32-x64 -Recurse -erroraction 'silentlycontinue'
Write-Output "Cleared all"

$ErrorActionPreference = "Stop"

mkdir build_scripts\win_build
Set-Location -Path ".\build_scripts\win_build" -PassThru

#git status

Write-Output "   ---"
Write-Output "curl miniupnpc"
Write-Output "   ---"
Invoke-WebRequest -Uri "https://pypi.skynet-network.org/v01/miniupnpc/miniupnpc-2.2.2-cp39-cp39-win_amd64.whl" -OutFile "miniupnpc-2.2.2-cp39-cp39-win_amd64.whl"
Write-Output "Using win_amd64 python 3.9 wheel from https://github.com/miniupnp/miniupnp/pull/475 (2.2.0-RC1)"
Write-Output "Actual build from https://github.com/miniupnp/miniupnp/commit/7783ac1545f70e3341da5866069bde88244dd848"
If ($LastExitCode -gt 0){
    Throw "Failed to download miniupnpc!"
}
else
{
    Set-Location -Path ..\..\ -PassThru
    Write-Output "miniupnpc download successful."
}

Write-Output "   ---"
Write-Output "Create venv - python3.9 is required in PATH"
Write-Output "   ---"
python -m venv venv
. .\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install wheel pep517
pip install pywin32
pip install pyinstaller==4.5
pip install setuptools_scm

Write-Output "   ---"
Write-Output "Get SKYNET_INSTALLER_VERSION"
# The environment variable SKYNET_INSTALLER_VERSION needs to be defined
$env:SKYNET_INSTALLER_VERSION = python .\build_scripts\installer-version.py -win

if (-not (Test-Path env:SKYNET_INSTALLER_VERSION)) {
  $env:SKYNET_INSTALLER_VERSION = '0.0.0'
  Write-Output "WARNING: No environment variable SKYNET_INSTALLER_VERSION set. Using 0.0.0"
  }
Write-Output "Skynet Version is: $env:SKYNET_INSTALLER_VERSION"
Write-Output "   ---"

Write-Output "   ---"
Write-Output "Build skynet-blockchain wheels"
Write-Output "   ---"
pip wheel --use-pep517 --extra-index-url https://pypi.skynet-network.org/v01/ -f . --wheel-dir=.\build_scripts\win_build .

Write-Output "   ---"
Write-Output "Install skynet-blockchain wheels into venv with pip"
Write-Output "   ---"

Write-Output "pip install miniupnpc"
Set-Location -Path ".\build_scripts" -PassThru
pip install --no-index --find-links=.\win_build\ miniupnpc
# Write-Output "pip install setproctitle"
# pip install setproctitle==1.2.2

Write-Output "pip install skynet-blockchain"
pip install --no-index --find-links=.\win_build\ skynet-blockchain

Write-Output "   ---"
Write-Output "Use pyinstaller to create skynet .exe's"
Write-Output "   ---"
$SPEC_FILE = (python -c 'import skynet; print(skynet.PYINSTALLER_SPEC_PATH)') -join "`n"
Write-Output "$SPEC_FILE"
pyinstaller --log-level INFO $SPEC_FILE

Write-Output "   ---"
Write-Output "Copy skynet executables to skynet-blockchain-gui\"
Write-Output "   ---"
Copy-Item "dist\daemon" -Destination "..\skynet-blockchain-gui\" -Recurse
Set-Location -Path "..\skynet-blockchain-gui" -PassThru

#git status

Write-Output "   ---"
Write-Output "Prepare Electron packager"
Write-Output "   ---"
$Env:NODE_OPTIONS = "--max-old-space-size=4000"
npm install --save-dev electron-winstaller
npm install -g electron-packager
npm install
npm audit fix

#git status

Write-Output "   ---"
Write-Output "Electron package Windows Installer"
Write-Output "   ---"
./node_modules/.bin/electron-rebuild -f -w node-pty
npm run build
If ($LastExitCode -gt 0){
    Throw "npm run build failed!"
}

# sets the version for skynet-blockchain in package.json
cp package.json package.json.orig
(Get-Content ".\package.json") -replace 'version": ".*?"', ('version": "' + $env:SKYNET_INSTALLER_VERSION + '"') | Set-Content ".\package.json"

Write-Output "   ---"
Write-Output "Increase the stack for skynet command for (skynet plots create) skynetpos limitations"
# editbin.exe needs to be in the path
# C:\msvs_tools\editbin.exe /STACK:8000000 daemon\skynet.exe
editbin.exe /STACK:8000000 daemon\skynet.exe
Write-Output "   ---"

$packageVersion = "$env:SKYNET_INSTALLER_VERSION"
$packageName = "Skynet-$packageVersion"

Write-Output "packageName is $packageName"

Write-Output "   ---"
Write-Output "electron-packager"
electron-packager . Skynet --asar.unpack="**\daemon\**" --overwrite --icon=.\src\assets\img\skynet.ico --app-version=$packageVersion --platform=win32 --arch=x64 
Write-Output "   ---"

Write-Output "   ---"
Write-Output "patch installer loader image"
Copy-Item "src\assets\img\skynet_loading_boxed.gif" -Destination "node_modules\electron-winstaller\resources\install-spinner.gif"
Write-Output "   ---"
Write-Output "node winstaller.js"
node winstaller.js
Write-Output "   ---"

#git status

If ($env:HAS_SECRET) {
   Write-Output "   ---"
   Write-Output "Add timestamp and verify signature"
   Write-Output "   ---"
   signtool.exe timestamp /v /t http://timestamp.comodoca.com/ .\release-builds\windows-installer\SkynetSetup-$packageVersion.exe
   signtool.exe verify /v /pa .\release-builds\windows-installer\SkynetSetup-$packageVersion.exe
   }   Else    {
   Write-Output "Skipping timestamp and verify signatures - no authorization to install certificates"
}

#git status

deactivate
Set-Location -Path ..\ -PassThru


Write-Output "   ---"
Write-Output "Windows Installer complete"
Write-Output "   ---"
