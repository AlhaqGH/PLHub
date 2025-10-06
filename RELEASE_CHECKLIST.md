# 🚀 PLHub v0.5.1 Release Checklist

## ✅ Pre-Release Checklist

### Version Updates
- [x] Update `setup.py` version to 0.5.1
- [x] Update `plhub.py` version string to 0.5.1
- [x] Update `README.md` version references
- [x] Update `CHANGELOG.md` with v0.5.1 entry
- [x] Create `RELEASE_NOTES.md` for v0.5.1

### Documentation
- [x] Update all command examples to new syntax
- [x] Create installation documentation
- [x] Create migration guide
- [x] Create troubleshooting guide
- [x] Update Android documentation

### Testing
- [ ] Test `plhub --version` shows 0.5.1
- [ ] Test `plhub doctor` works
- [ ] Test `plhub build apk` syntax works
- [ ] Test installation scripts (install.bat, install.sh)
- [ ] Test PATH setup on fresh system
- [ ] Verify backward compatibility (python plhub.py still works)

### Code Quality
- [ ] Run linter on plhub.py
- [ ] Check for syntax errors
- [ ] Verify all imports work
- [ ] Test on Windows, Linux, macOS (if possible)

---

## 📦 Release Process

### 1. Commit Changes

```powershell
# Stage all changes
git add .

# Commit with version message
git commit -m "Release v0.5.1: Language-Independent Commands

- Add global CLI access with plhub command
- Add short platform names (apk, ipa, exe, app)
- Add automated installation scripts
- Add comprehensive documentation
- Update all command syntax throughout
- Maintain backward compatibility"

# Push to main branch
git push origin main
```

### 2. Create Git Tag

```powershell
# Create annotated tag
git tag -a v0.5.1 -m "PLHub v0.5.1 - Language-Independent Commands

Major Features:
- Global plhub command (no python prefix required)
- Short platform names: apk, ipa, exe, app, dmg
- Automated installation with PATH configuration
- Launcher scripts for all platforms
- Comprehensive documentation and guides
- Backward compatible with v0.5.0"

# Push tag to GitHub
git push origin v0.5.1
```

### 3. Create GitHub Release

Go to: https://github.com/AlhaqGH/PLHub/releases/new

**Tag:** `v0.5.1`

**Title:** `PLHub v0.5.1 - Language-Independent Commands`

**Description:** (Copy from RELEASE_NOTES.md)

**Assets to attach:**
- None required (users clone repo)

### 4. Update Repository Description

GitHub repository description:
```
PL-Hub: Professional development environment for PohLang with language-independent CLI, automated builds, Android APK builder, and comprehensive tooling
```

Topics to add:
- `pohlang`
- `development-environment`
- `cli-tool`
- `android-apk`
- `build-automation`
- `project-templates`

---

## 📢 Announcement

### Social Media Post Template

```
🎉 PLHub v0.5.1 Released!

Now with language-independent commands! 🚀

✨ What's new:
• Direct `plhub` command (no Python prefix!)
• Short syntax: `plhub build apk --release`
• Automated installation for all platforms
• Global accessibility from any directory

Just like git, npm, and docker! 💻

Download: https://github.com/AlhaqGH/PLHub/releases/tag/v0.5.1

#PLHub #PohLang #DevTools #CLI
```

### README Badge Update

Add release badge to README.md:
```markdown
![Version](https://img.shields.io/badge/version-0.5.1-blue)
![Release Date](https://img.shields.io/badge/release-Oct%206%2C%202025-green)
```

---

## 🐛 Post-Release

### Monitor for Issues
- [ ] Watch GitHub issues for bug reports
- [ ] Check installation feedback
- [ ] Monitor PATH setup problems
- [ ] Address documentation gaps

### Future Improvements (v0.5.2+)
- [ ] PyInstaller standalone executable
- [ ] Package registry enhancements
- [ ] Enhanced VS Code integration
- [ ] More platform templates
- [ ] Performance optimizations

---

## 📝 Quick Release Commands

### Full Release (Copy-Paste)

```powershell
# Navigate to PLHub directory
cd C:\Users\habib\POHLANG\PLHub

# Ensure all changes are saved
git status

# Add all changes
git add .

# Commit
git commit -m "Release v0.5.1: Language-Independent Commands"

# Create tag
git tag -a v0.5.1 -m "PLHub v0.5.1 - Language-Independent Commands"

# Push everything
git push origin main
git push origin v0.5.1

# Verify on GitHub
start https://github.com/AlhaqGH/PLHub/releases
```

### Verify Release

```powershell
# Clone fresh copy
cd C:\Temp
git clone https://github.com/AlhaqGH/PLHub.git
cd PLHub

# Run installer
.\install.bat

# Test commands (in new terminal)
plhub --version  # Should show v0.5.1
plhub doctor
plhub build apk --help
```

---

## ✅ Release Complete!

Once all steps are done:

1. ✅ Version updated to 0.5.1
2. ✅ Documentation complete
3. ✅ Code committed and pushed
4. ✅ Tag created and pushed
5. ✅ GitHub release published
6. ✅ Announcement posted

**🎊 Congratulations on releasing PLHub v0.5.1! 🎊**
