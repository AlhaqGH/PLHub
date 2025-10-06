# PLHub Cleanup Script
# Removes old Python runtime and ensures latest PohLang Rust runtime is used

Write-Host "🧹 PLHub Cleanup - Removing Old Runtime Files" -ForegroundColor Cyan
Write-Host "=" * 60

$ErrorActionPreference = "Continue"

# 1. Remove Runtime/transpiler (Dart transpiler, not needed - use Rust)
Write-Host "`n📁 Removing Runtime/transpiler..." -ForegroundColor Yellow
if (Test-Path "Runtime\transpiler") {
    Remove-Item -Recurse -Force "Runtime\transpiler"
    Write-Host "   ✅ Removed Runtime/transpiler" -ForegroundColor Green
} else {
    Write-Host "   ⏭️  Runtime/transpiler already removed" -ForegroundColor Gray
}

# 2. Remove plhub-sdk/Runtime/Interpreter (Python interpreter in SDK)
Write-Host "`n📁 Removing plhub-sdk/Runtime/Interpreter..." -ForegroundColor Yellow
if (Test-Path "plhub-sdk\Runtime\Interpreter") {
    Remove-Item -Recurse -Force "plhub-sdk\Runtime\Interpreter"
    Write-Host "   ✅ Removed plhub-sdk/Runtime/Interpreter" -ForegroundColor Green
} else {
    Write-Host "   ⏭️  plhub-sdk/Runtime/Interpreter already removed" -ForegroundColor Gray
}

# 3. Remove plhub-sdk/Runtime/transpiler (Dart transpiler in SDK)
Write-Host "`n📁 Removing plhub-sdk/Runtime/transpiler..." -ForegroundColor Yellow
if (Test-Path "plhub-sdk\Runtime\transpiler") {
    Remove-Item -Recurse -Force "plhub-sdk\Runtime\transpiler"
    Write-Host "   ✅ Removed plhub-sdk/Runtime/transpiler" -ForegroundColor Green
} else {
    Write-Host "   ⏭️  plhub-sdk/Runtime/transpiler already removed" -ForegroundColor Gray
}

# 4. Clean up any __pycache__ directories
Write-Host "`n📁 Cleaning up __pycache__ directories..." -ForegroundColor Yellow
$pycacheDirs = Get-ChildItem -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue
if ($pycacheDirs) {
    foreach ($dir in $pycacheDirs) {
        Remove-Item -Recurse -Force $dir.FullName -ErrorAction SilentlyContinue
        Write-Host "   ✅ Removed $($dir.FullName)" -ForegroundColor Green
    }
} else {
    Write-Host "   ⏭️  No __pycache__ directories found" -ForegroundColor Gray
}

# 5. Clean up *.pyc files
Write-Host "`n📁 Cleaning up *.pyc files..." -ForegroundColor Yellow
$pycFiles = Get-ChildItem -Recurse -File -Filter "*.pyc" -ErrorAction SilentlyContinue
if ($pycFiles) {
    foreach ($file in $pycFiles) {
        Remove-Item -Force $file.FullName -ErrorAction SilentlyContinue
        Write-Host "   ✅ Removed $($file.FullName)" -ForegroundColor Green
    }
} else {
    Write-Host "   ⏭️  No *.pyc files found" -ForegroundColor Gray
}

# 6. Show what remains in Runtime/
Write-Host "`n📊 Current Runtime/ structure:" -ForegroundColor Yellow
if (Test-Path "Runtime") {
    Get-ChildItem "Runtime" -Directory | ForEach-Object {
        Write-Host "   📁 Runtime/$($_.Name)" -ForegroundColor Cyan
    }
    Get-ChildItem "Runtime" -File | ForEach-Object {
        Write-Host "   📄 Runtime/$($_.Name)" -ForegroundColor White
    }
}

# 7. Show what remains in plhub-sdk/Runtime/
Write-Host "`n📊 Current plhub-sdk/Runtime/ structure:" -ForegroundColor Yellow
if (Test-Path "plhub-sdk\Runtime") {
    Get-ChildItem "plhub-sdk\Runtime" -Directory | ForEach-Object {
        Write-Host "   📁 plhub-sdk/Runtime/$($_.Name)" -ForegroundColor Cyan
    }
    Get-ChildItem "plhub-sdk\Runtime" -File | ForEach-Object {
        Write-Host "   📄 plhub-sdk/Runtime/$($_.Name)" -ForegroundColor White
    }
}

Write-Host "`n✅ Cleanup completed!" -ForegroundColor Green
Write-Host "`n📝 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Review changes: git status" -ForegroundColor White
Write-Host "   2. Update code to remove Python interpreter references" -ForegroundColor White
Write-Host "   3. Test with: python -m unittest discover -s Tests -v" -ForegroundColor White
Write-Host "   4. Commit changes: git add -A && git commit -m 'Remove old Python runtime, use Rust only'" -ForegroundColor White
Write-Host "   5. Update SDK: python tools/update_sdk.py --sync" -ForegroundColor White
