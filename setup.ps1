# Create .env file
Write-Host "Creating .env file..." -ForegroundColor Green
if (!(Test-Path -Path "./.env")) {
    New-Item -Path . -Name ".\.env" -ItemType "file" -Value (
        'PASSWORD = "password_here"' + [System.Environment]::NewLine + 
        'UNAME = "username here"' + [System.Environment]::NewLine + 
        'DBNAME = "database name here"' + [System.Environment]::NewLine + 
        'PORT = "port number here"')
} 

# Create Venv
Write-Host "Creating Venv Directory..." -ForegroundColor Green
if (!(Test-Path -Path './.venv')) {
    mkdir ./.venv/
} 

Write-Host "Creating Venv..." -ForegroundColor Green
py -3.12 -m venv ./.venv

Write-Host "Installing Required Packages in Venv..." -ForegroundColor green
$pythonVenvLoc=Get-ChildItem python.exe -Recurse -ErrorAction Stop
$pyVenvFull = $pythonVenvLoc.FullName

# Install dependencies
Start-Process -NoNewWindow -FilePath $pyVenvFull -Wait -ArgumentList "-m pip install --upgrade pip"
Start-Process -NoNewWindow -FilePath $pyVenvFull -Wait -ArgumentList "-m pip install -r ./requirements.txt"

Write-Host "Done!" -ForegroundColor Green