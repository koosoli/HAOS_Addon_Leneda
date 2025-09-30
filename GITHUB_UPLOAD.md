# 🚀 Quick Start - Upload to GitHub

## Step 1: Initialize Git Repository

Open PowerShell and run:

```powershell
cd "c:\Users\mail\Downloads\haos hello word addon project\HAOS_Addon_Leneda"
git init
git add .
git commit -m "Initial release - Leneda Energy Dashboard v0.1.0

Features:
- Real-time energy monitoring with 15-minute intervals
- Dark mode dashboard with Chart.js visualizations
- Invoice calculator with Luxembourg tariffs
- Solar production tracking
- Auto-refresh functionality
- Responsive design
- Home Assistant ingress integration"
```

## Step 2: Link to GitHub

```powershell
git branch -M main
git remote add origin https://github.com/koosoli/HAOS_Addon_Leneda.git
git push -u origin main
```

## Step 3: Add to Home Assistant

1. Open Home Assistant
2. Go to **Settings** → **Add-ons** → **Add-on Store**
3. Click the **⋮** menu (top right)
4. Select **Repositories**
5. Add this URL:
   ```
   https://github.com/koosoli/HAOS_Addon_Leneda
   ```
6. Click **Add**
7. Refresh the page
8. Find **"Leneda Energy Dashboard"** in the store
9. Click **Install**

## Step 4: Configure

After installation:

1. Click on the addon
2. Go to **Configuration** tab
3. Add your credentials:

```yaml
api_key: "your_leneda_api_key"
energy_id: "your_leneda_energy_id"
metering_points:
  - code: "LU000000100000000000000070056600"
    name: "Main Meter"
    type: "consumption"
```

4. Click **Save**
5. Go to **Info** tab
6. Click **Start**
7. Wait for it to start (check logs if needed)
8. Click **Open Web UI** or find it in your sidebar!

## Getting Your Credentials

1. Go to https://portal.leneda.eu
2. Log in to your account
3. Navigate to **Settings** → **API Keys**
4. Click **Generate New API Key**
5. Copy your:
   - **API Key**
   - **Energy ID**
   - **Metering Point Code(s)**

## Troubleshooting

### If the addon doesn't start:
```powershell
# Check the logs in Home Assistant
Settings → Add-ons → Leneda Energy Dashboard → Log
```

### If you need to rebuild:
```powershell
# Make changes to the code
git add .
git commit -m "Fix: description of changes"
git push

# Then in Home Assistant:
# Uninstall → Reinstall → Start
```

## Done! 🎉

Your Leneda Energy Dashboard should now be running!

Access it from:
- Home Assistant sidebar: **"Leneda Energy"**
- Or click **"Open Web UI"** in the addon page

Enjoy monitoring your energy! ⚡
