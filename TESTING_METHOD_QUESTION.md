# 🔍 CRITICAL QUESTION - Testing Method

## I NEED TO KNOW: How are you testing this addon?

There are TWO different ways to test Home Assistant addons:

### METHOD 1: LOCAL ADDON (Manual Copy) 📁
- Copy addon folder to Home Assistant's `/addons` directory
- Access via Samba share (`\\homeassistant\addons\`) or SSH
- Shows up as "Local add-ons" in the store
- **NO GitHub repository needed**
- **NO repository.json needed**

**For local testing:**
```
/addons/
└── leneda_dashboard/         ← Copy this entire folder
    ├── config.yaml
    ├── Dockerfile
    ├── run.sh
    └── rootfs/
```

### METHOD 2: GITHUB REPOSITORY 🌐
- Push addon to GitHub
- Add repository URL in Home Assistant
- Home Assistant downloads from GitHub
- **Requires repository.json in root**

**For GitHub testing:**
```
Your GitHub Repo/
├── repository.json           ← Required!
└── leneda_dashboard/
    ├── config.yaml
    ├── Dockerfile  
    ├── run.sh
    └── rootfs/
```

## ❓ PLEASE TELL ME:

1. **Are you copying the addon to Home Assistant's `/addons` folder?** (LOCAL)
2. **Or are you adding a GitHub repository URL?** (REMOTE)

This makes a HUGE difference in troubleshooting!

---

## If Testing LOCALLY:

You should copy ONLY the `leneda_dashboard/` folder to `/addons/`:

```
Via Samba: \\homeassistant\addons\leneda_dashboard\
Via SSH: /addons/leneda_dashboard/
```

Then refresh the add-on store.

## If Testing from GITHUB:

You need to:
1. Push entire HAOS_Addon_Leneda folder to GitHub
2. In HA: Settings → Add-ons → Add-on Store → ⋮ → Repositories
3. Add: `https://github.com/koosoli/HAOS_Addon_Leneda`
4. Refresh store

---

**WHICH METHOD ARE YOU USING?** This is critical to solving the issue!
