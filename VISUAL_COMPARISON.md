# 📊 VISUAL COMPARISON - Before vs After

## THE CRITICAL DIFFERENCE

```
╔════════════════════════════════════════════════════════════════════════╗
║                    HELLO WORLD (WORKING ✅)                            ║
╚════════════════════════════════════════════════════════════════════════╝

hello_world/
├── 📄 config.yaml       ← Addon metadata
├── 🐳 Dockerfile        ← Build instructions
├── ▶️  run.sh           ← ✅ STARTUP SCRIPT IN ROOT!
└── 📁 rootfs/
    └── 📁 www/
        └── 📄 index.html

Dockerfile says:
   COPY run.sh /run.sh   ← ✅ Finds run.sh in hello_world/run.sh


╔════════════════════════════════════════════════════════════════════════╗
║                  LENEDA v1 - BROKEN ❌                                 ║
╚════════════════════════════════════════════════════════════════════════╝

leneda_dashboard/
├── 📄 config.yaml       ← Addon metadata
├── 🐳 Dockerfile        ← Build instructions
└── 📁 rootfs/
    └── 📁 app/
        ├── ▶️  run.sh   ← ❌ STARTUP SCRIPT IN WRONG PLACE!
        └── 🐍 server.py

Dockerfile says:
   COPY run.sh /run.sh   ← ❌ Can't find run.sh in leneda_dashboard/
                         ← ❌ BUILD FAILS!
                         ← ❌ ADDON NOT DISCOVERABLE!


╔════════════════════════════════════════════════════════════════════════╗
║                  LENEDA v2 - FIXED ✅                                  ║
╚════════════════════════════════════════════════════════════════════════╝

leneda_dashboard/
├── 📄 config.yaml       ← Addon metadata
├── 🐳 Dockerfile        ← Build instructions
├── ▶️  run.sh           ← ✅ STARTUP SCRIPT IN ROOT! (FIXED!)
├── 🎨 icon.svg          ← Branding
├── 🎨 logo.svg          ← Branding
└── 📁 rootfs/
    └── 📁 app/
        ├── 🐍 server.py
        └── 📁 static/
            ├── 📄 index.html
            ├── 🎨 styles.css
            └── 📜 app.js

Dockerfile says:
   COPY run.sh /run.sh   ← ✅ Finds run.sh in leneda_dashboard/run.sh
                         ← ✅ BUILD SUCCEEDS!
                         ← ✅ ADDON IS DISCOVERABLE!
```

## THE BUILD PROCESS

```
╔════════════════════════════════════════════════════════════════════════╗
║                  DOCKER BUILD CONTEXT                                  ║
╚════════════════════════════════════════════════════════════════════════╝

When Dockerfile runs "COPY run.sh /run.sh", Docker looks in:

leneda_dashboard/          ← BUILD CONTEXT ROOT
├── run.sh                ← ✅ Docker finds THIS file
└── rootfs/
    └── app/
        └── run.sh        ← ❌ Docker CANNOT find this as "run.sh"
                          ← (This would be "rootfs/app/run.sh")

To copy from rootfs, you must specify the full path:
   COPY rootfs/app/run.sh /run.sh   ← This would work
   COPY run.sh /run.sh              ← This expects run.sh in root!
```

## THE HOME ASSISTANT DISCOVERY FLOW

```
╔════════════════════════════════════════════════════════════════════════╗
║              HOME ASSISTANT DISCOVERY PROCESS                          ║
╚════════════════════════════════════════════════════════════════════════╝

1. 📥 User adds repository URL
   └─> HA fetches repository.json
       └─> ✅ Valid JSON found

2. 🔍 HA scans repository for addons
   └─> Looks for directories with config.yaml
       └─> ✅ Found: leneda_dashboard/config.yaml

3. ✔️  HA validates config.yaml
   └─> Checks required fields (name, version, slug, arch)
       └─> ✅ All valid!

4. 🐳 HA attempts to build Docker image
   ┌─────────────────────────────────────────────────────────────┐
   │ FROM python:3.11-alpine          ✅ Base image exists       │
   │ RUN pip install flask requests   ✅ Packages install        │
   │ COPY rootfs/app /app             ✅ Files copied            │
   │ COPY run.sh /run.sh              ❓ THIS IS THE KEY STEP!   │
   │                                                              │
   │ WITH BROKEN STRUCTURE:                                       │
   │ └─> ❌ ERROR: run.sh not found                              │
   │     └─> ❌ BUILD FAILS                                       │
   │         └─> ❌ ADDON EXCLUDED FROM STORE                     │
   │                                                              │
   │ WITH FIXED STRUCTURE:                                        │
   │ └─> ✅ run.sh found in leneda_dashboard/                    │
   │     └─> ✅ File copied successfully                          │
   │         └─> ✅ BUILD SUCCEEDS!                               │
   │             └─> ✅ ADDON APPEARS IN STORE!                   │
   └─────────────────────────────────────────────────────────────┘

5. 📦 Result
   ├── ❌ BROKEN: Addon not listed (build failed)
   └── ✅ FIXED:  Addon appears in "Local add-ons" section!
```

## FILE PLACEMENT RULES

```
╔════════════════════════════════════════════════════════════════════════╗
║                   WHERE FILES SHOULD GO                                ║
╚════════════════════════════════════════════════════════════════════════╝

📁 addon_name/                      ← ADDON ROOT
├── 📄 config.yaml                 ← ✅ HERE (addon configuration)
├── 🐳 Dockerfile                   ← ✅ HERE (build instructions)
├── ▶️  run.sh                      ← ✅ HERE (startup script)
├── 🎨 icon.png/svg                 ← ✅ HERE (addon icon)
├── 🎨 logo.png/svg                 ← ✅ HERE (addon logo)
├── 📄 README.md                    ← ✅ HERE (documentation)
├── 📄 DOCS.md                      ← ✅ HERE (full documentation)
├── 📄 CHANGELOG.md                 ← ✅ HERE (version history)
├── 🔧 build.yaml                   ← ✅ HERE (optional build config)
└── 📁 rootfs/                      ← APPLICATION FILES FOLDER
    ├── 📁 app/                     ← Your application code
    │   ├── 🐍 server.py           ← ✅ HERE (runtime file)
    │   └── 📁 static/             ← ✅ HERE (web assets)
    ├── 📁 etc/                     ← Config files copied to /etc
    ├── 📁 usr/                     ← Binaries copied to /usr
    └── 📁 var/                     ← Variable data

RULE OF THUMB:
├── Addon ROOT    = Files needed for HA to build/configure addon
└── rootfs/       = Files copied into the running container
```

## WHAT HAPPENS AT RUNTIME

```
╔════════════════════════════════════════════════════════════════════════╗
║                  CONTAINER FILESYSTEM AT RUNTIME                       ║
╚════════════════════════════════════════════════════════════════════════╝

After build completes, the container has:

/                           ← Container root
├── run.sh                 ← Copied from addon_root/run.sh
├── app/                   ← Copied from addon_root/rootfs/app/
│   ├── server.py
│   └── static/
│       ├── index.html
│       ├── styles.css
│       └── app.js
├── data/                  ← Mounted by HA (persistent storage)
│   └── options.json      ← User configuration
└── ...other system dirs

Then CMD ["/run.sh"] executes:
   /run.sh
   └─> cd /app
       └─> exec python3 server.py
           └─> Flask starts on port 8099
               └─> Ingress proxies traffic
                   └─> User sees dashboard! 🎉
```

## SUMMARY

```
╔════════════════════════════════════════════════════════════════════════╗
║                        KEY TAKEAWAY                                    ║
╚════════════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│  run.sh MUST be in the addon root directory,                          │
│  NOT inside the rootfs/ folder!                                        │
│                                                                        │
│  ✅ addon_name/run.sh          ← CORRECT                              │
│  ❌ addon_name/rootfs/app/run.sh   ← WRONG                            │
│                                                                        │
│  This is because the Dockerfile copies from the addon root            │
│  build context, and "COPY run.sh" expects the file there.             │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘

                         NOW FIXED! ✅
```

---
**Visual Guide Created:** September 30, 2025  
**Purpose:** Clearly illustrate the structural fix  
**Status:** All issues resolved ✅
