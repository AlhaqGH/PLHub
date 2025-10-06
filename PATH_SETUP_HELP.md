# 🔧 Quick Fix: PLHub Command Not Found

If you see `plhub: command not found` or `plhub is not recognized`, this means the PATH environment variable hasn't been updated in your current session.

## ✅ Solutions

### Option 1: Restart Terminal (Recommended)

The simplest solution:

1. **Close** your current PowerShell/Terminal window
2. **Open** a new PowerShell/Terminal window
3. Test: `plhub --version`

**This is the recommended approach** - it ensures all environment changes take effect properly.

---

### Option 2: Reload PATH in Current Session

If you don't want to restart:

**PowerShell:**
```powershell
# Add PLHub to PATH for this session only
$env:PATH += ";C:\Users\habib\POHLANG\PLHub"

# Test
plhub --version
```

**Note:** This only affects the current session. New windows will work automatically.

---

### Option 3: Use Local Path

Until you restart, you can call plhub.bat directly:

```powershell
# From PLHub directory
cd C:\Users\habib\POHLANG\PLHub
.\plhub.bat --version
.\plhub.bat doctor
.\plhub.bat build apk --release

# From any directory (full path)
C:\Users\habib\POHLANG\PLHub\plhub.bat run app.poh
```

---

### Option 4: Run Setup Helper

We've created a helper script that adds PLHub to PATH:

```powershell
cd C:\Users\habib\POHLANG\PLHub
.\setup-path.ps1
```

This will:
- ✅ Verify plhub.bat exists
- ✅ Add PLHub to user PATH (if not already)
- ✅ Update current session PATH
- ✅ Test the command

---

## 🔍 Verify Installation

Check if PLHub is in your PATH:

```powershell
# View PATH entries containing "PLHub"
$env:PATH -split ';' | Select-String -Pattern 'PLHub'

# Expected output:
# C:\Users\habib\POHLANG\PLHub
```

If you see the path, then restart your terminal and it will work!

---

## 🐛 Troubleshooting

### PATH Not Updated After Installation

If `install.bat` ran but PATH wasn't updated:

```powershell
# Run install.bat again
cd C:\Users\habib\POHLANG\PLHub
.\install.bat

# Or manually add to PATH
[Environment]::SetEnvironmentVariable(
    "Path", 
    [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Users\habib\POHLANG\PLHub",
    "User"
)
```

### Virtual Environment Conflict

If you're in a Python virtual environment (`.venv`), it might interfere:

```powershell
# Deactivate virtual environment
deactivate

# Test plhub command
plhub --version

# Or add PLHub to PATH before activating venv
$env:PATH = "C:\Users\habib\POHLANG\PLHub;" + $env:PATH
& .venv\Scripts\Activate.ps1
plhub --version
```

### PowerShell Execution Policy

If you get "script execution disabled" errors:

```powershell
# Check current policy
Get-ExecutionPolicy

# Allow local scripts (as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for one script
PowerShell -ExecutionPolicy Bypass -File setup-path.ps1
```

---

## ✅ Verification Commands

After fixing PATH, test these commands:

```powershell
# Check version
plhub --version

# Check environment
plhub doctor

# Build APK (from android-calculator directory)
cd C:\Users\habib\POHLANG\PLHub\Examples\android-calculator
plhub build apk

# Run example
cd C:\Users\habib\POHLANG\PLHub
plhub run examples\poh\hello.poh
```

All should work without `python` prefix! ✨

---

## 📝 Summary

**The installation worked correctly!** The PATH was updated, but:

1. **Your current PowerShell session** doesn't see the new PATH yet
2. **Solution:** Close and reopen PowerShell/Terminal
3. **Alternative:** Run `$env:PATH += ";C:\Users\habib\POHLANG\PLHub"`

**After restart, you can use:**
- `plhub --version`
- `plhub doctor`
- `plhub build apk --release`
- `plhub run app.poh`

🎉 **Your PLHub is installed correctly and ready to use!**

---

## 🚀 Next Steps

Once `plhub` command works:

1. **Verify environment**: `plhub doctor`
2. **Try examples**: `plhub run examples\poh\hello.poh`
3. **Build APK**: `cd Examples\android-calculator && plhub build apk`
4. **Read docs**: See `INSTALL_AND_USAGE.md` for complete reference

**Welcome to PLHub with language-independent commands!** 🎊
