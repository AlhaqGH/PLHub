# PohLang Extensions Quick Reference

## 📦 Two Extensions, One Experience

### 🎨 PohLang Language Support
**What it does**: Makes `.poh` files look pretty and smart  
**Version**: 0.3.1  
**Install**: `code --install-extension pohlang.pohlang`

**Features**:
- ✅ Syntax highlighting (colors!)
- ✅ Code snippets (templates)
- ✅ IntelliSense (auto-complete)
- ✅ Hover docs (tooltips)
- ✅ Error detection (red squiggles)

---

### ⚡ PLHub
**What it does**: Runs your code and manages projects  
**Version**: 0.2.3  
**Install**: `code --install-extension pohlang.plhub`

**Features**:
- ✅ Run files (Ctrl+F5)
- ✅ Create projects
- ✅ Update runtime
- ✅ Manage versions
- ✅ SDK integration

---

## 🚀 Quick Start (1 Minute)

### Install Both Extensions
```powershell
# Language support (syntax highlighting)
code --install-extension pohlang.pohlang

# PLHub (run code)
code --install-extension pohlang.plhub
```

### Write Your First Program
```pohlang
# hello.poh
Write "Hello, PohLang!"
```

### Run It
Press **Ctrl+F5** or right-click → **PL-Hub: Run File**

---

## 🎯 Which Extension Do I Need?

| Task | Language Extension | PLHub Extension |
|------|-------------------|-----------------|
| View .poh files with colors | ✅ | ❌ |
| Get code suggestions | ✅ | ❌ |
| Run .poh files | ❌ | ✅ |
| Create projects | ❌ | ✅ |
| Update PohLang | ❌ | ✅ |

**Answer**: Install **BOTH** for full experience! 🎉

---

## 📋 Current Versions

| Component | Version | Status |
|-----------|---------|--------|
| PohLang Runtime | v0.6.0 | Latest |
| Language Extension | v0.3.1 | Latest |
| PLHub Extension | v0.2.3 | Latest |

**All updated**: October 12, 2025

---

## 🔧 Common Commands

### PL-Hub Commands (Ctrl+Shift+P)
- `PL-Hub: Run File` - Execute current .poh file (Ctrl+F5)
- `PL-Hub: Create Project` - Start new PohLang project
- `PL-Hub: Update Language` - Get latest runtime
- `PL-Hub: Show SDK Versions` - Check installed versions

---

## ❓ Troubleshooting

### No syntax highlighting?
**Fix**: Install Language Extension
```powershell
code --install-extension pohlang.pohlang
```

### Can't run files?
**Fix**: Install PLHub Extension
```powershell
code --install-extension pohlang.plhub
```

### Extensions conflicting?
**Fix**: Update both to latest versions
```powershell
code --install-extension pohlang.pohlang --force
code --install-extension pohlang.plhub --force
```

---

## 📖 More Info

- **Full Guide**: See `EXTENSION_SEPARATION.md`
- **Versions**: See `VERSION_COMPATIBILITY.md`
- **Changelog**: Check extension CHANGELOG.md files
- **Issues**: https://github.com/AlhaqGH/PohLang/issues

---

**TL;DR**: Install both extensions, press Ctrl+F5 to run code. That's it! 🚀
