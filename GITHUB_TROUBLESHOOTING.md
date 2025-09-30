# 🔍 GITHUB REPOSITORY TROUBLESHOOTING

## ✅ VERIFIED: Repository Structure is CORRECT on GitHub!

I checked your GitHub repository and confirmed:
- ✅ `run.sh` exists in `leneda_dashboard/` (addon root)
- ✅ `Dockerfile` exists
- ✅ `config.yaml` exists  
- ✅ `rootfs/app/` folder exists
- ✅ `repository.json` exists in repo root

**The structure on GitHub is CORRECT!**

---

## 🔧 HOME ASSISTANT TROUBLESHOOTING

Since the structure is correct, the issue must be with how Home Assistant is reading it.

### Step 1: Clear Home Assistant Cache

1. **In Home Assistant:**
   - Settings → Add-ons → Add-on Store
   - Top right menu (⋮) → Repositories
   - Find your repository: `https://github.com/koosoli/HAOS_Addon_Leneda`
   - Click on it
   - Click "REMOVE" (don't worry, this just removes the link)

2. **Clear browser cache:**
   - Press `Ctrl + Shift + Delete` (Windows/Linux)
   - Or `Cmd + Shift + Delete` (macOS)
   - Clear "Cached images and files"

3. **Re-add repository:**
   - Settings → Add-ons → Add-on Store
   - Top right menu (⋮) → Repositories
   - Click "ADD REPOSITORY"
   - Enter: `https://github.com/koosoli/HAOS_Addon_Leneda`
   - Click "ADD"

4. **Refresh:**
   - Click "Check for updates" in top right menu
   - Press `F5` to refresh browser
   - Wait 30 seconds

### Step 2: Check Supervisor Logs

**This is CRITICAL** - the logs will tell us exactly what's wrong:

1. Go to: Settings → System → Logs
2. Select "Supervisor" from the dropdown (top right)
3. Scroll to the bottom
4. Look for errors related to:
   - `HAOS_Addon_Leneda`
   - `leneda_dashboard`
   - YAML validation errors
   - Docker build errors

**PLEASE COPY THE RELEVANT LOG LINES AND SHARE THEM!**

### Step 3: Verify Repository URL

Make sure you're adding the EXACT URL:
```
https://github.com/koosoli/HAOS_Addon_Leneda
```

**NOT:**
- ❌ `https://github.com/koosoli/HAOS_Addon_Leneda.git`
- ❌ `https://github.com/koosoli/HAOS_Addon_Leneda/`
- ❌ `https://github.com/koosoli/HAOS_Addon_Leneda/tree/main`

### Step 4: Check Home Assistant Version

What version of Home Assistant are you running?
- Settings → System → About
- Core version: ?
- Supervisor version: ?

Some older versions have issues with addon discovery.

---

## 🧪 ALTERNATIVE: Test Locally First

To eliminate GitHub as a variable, test locally:

### Method A: Via Samba (Easiest)

1. Install Samba add-on from Home Assistant store
2. Start Samba
3. On your PC, open: `\\homeassistant\addons\`
4. Create folder: `leneda_dashboard`
5. Copy ALL files from your local `leneda_dashboard/` folder to this network share
6. In HA, go to Add-on Store → "Check for updates"
7. Should appear under "Local add-ons"

### Method B: Via SSH

1. Install SSH add-on
2. SSH to Home Assistant
3. Navigate to `/addons/`
4. Create folder: `mkdir -p /addons/leneda_dashboard`
5. Upload files (use SCP or SFTP)
6. Refresh add-on store

---

## 📋 COMMON ISSUES & SOLUTIONS

### Issue: "Invalid YAML"
**Solution:** Validate your `config.yaml`:
- Go to: http://www.yamllint.com/
- Paste your config.yaml content
- Fix any errors

### Issue: "Build failed"
**Solution:** Check Dockerfile:
- Make sure `run.sh` exists in addon root
- Verify Python packages install correctly

### Issue: "Repository not found"
**Solution:**
- Make sure repo is PUBLIC (not private)
- Verify URL is correct
- Check internet connectivity

### Issue: "Addon appears then disappears"
**Solution:**
- This means validation failed AFTER loading
- Check Supervisor logs for specific error
- Usually a schema/options mismatch

---

## 🎯 WHAT TO DO RIGHT NOW

1. ✅ **Remove and re-add the repository** (clear cache)
2. ✅ **Check Supervisor logs** (this will tell us the EXACT error)
3. ✅ **Share the log output** with me

The logs will show us EXACTLY what Home Assistant doesn't like!

---

## 📊 EXPECTED vs REALITY

### What SHOULD happen:
```
[INFO] Loading repository https://github.com/koosoli/HAOS_Addon_Leneda
[INFO] Found addon: leneda_dashboard
[INFO] Validating config for leneda_dashboard
[INFO] Config valid, addon available
```

### If validation fails:
```
[ERROR] Invalid config for leneda_dashboard
[ERROR] Schema validation failed: <specific error>
```

### If build fails:
```
[ERROR] Failed to build leneda_dashboard
[ERROR] Docker build error: <specific error>
```

**These logs are the key to solving this!**

---

## 🆘 PLEASE PROVIDE:

1. **Supervisor logs** (last 50-100 lines after adding repository)
2. **Home Assistant version**
3. **Exact error message** (if visible in UI)
4. **Screenshot** of add-on store after refresh

With this information, I can pinpoint the EXACT issue!

---

**Date:** September 30, 2025  
**Status:** Structure verified correct on GitHub  
**Next Step:** Check Home Assistant logs for discovery error
