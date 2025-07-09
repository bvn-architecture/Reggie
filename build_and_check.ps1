# Build and Check Script for PyPI Upload
# This script copies the PyPI config, cleans old builds, builds the package, checks it, and uploads to PyPI

Write-Host "Copying .pypirc configuration..." -ForegroundColor Green
Copy-Item .pypirc.txt $env:USERPROFILE\.pypirc

Write-Host "Cleaning old build artifacts..." -ForegroundColor Green
Remove-Item -Path "dist", "build", "*.egg-info" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Building package..." -ForegroundColor Green
python -m build

Write-Host "Checking distribution files..." -ForegroundColor Green
python -m twine check dist/*

Write-Host "Uploading to PyPI..." -ForegroundColor Green
python -m twine upload dist/*

Write-Host "Upload complete!" -ForegroundColor Green
