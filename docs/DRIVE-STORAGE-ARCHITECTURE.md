# Google Drive Storage Architecture - Cloud-First Backend

**Unlimited Storage + Automatic Multi-Device Sync**

---

## 🎯 Vision

**Replace local filesystem with Google Drive as primary storage backend.**

### Why Drive?

1. **Unlimited Storage** - Red Hat Workspace accounts = unlimited Drive storage
2. **Multi-Device Sync** - Automatic sync across laptop, desktop, tablet
3. **Version History** - Drive tracks all file versions automatically
4. **Team Sharing** - Share customer folders with other TAMs
5. **Automatic Backup** - No manual backup needed
6. **Mobile Access** - Access data from phone/tablet
7. **Offline Support** - Drive apps work offline with local cache

---

## 🏗️ Architecture

### Before (Local Filesystem)
```
~/Documents/rh/
├── td-bank/
│   ├── customer.yaml
│   └── reports/
│       └── 2025-10-report.md
└── wells-fargo/
    └── ...

Problems:
❌ No sync between devices
❌ Manual backup required
❌ Limited disk space
❌ No version history
❌ No team sharing
```

### After (Google Drive)
```
Drive://Taminator/
├── customers/
│   ├── td-bank/
│   │   ├── customer.yaml
│   │   └── reports/
│   │       └── 2025-10-report.md
│   └── wells-fargo/
│       └── ...
├── settings/
│   └── settings.json (synced across devices!)
└── templates/
    └── report-templates/

Benefits:
✅ Auto-sync across all devices
✅ Unlimited storage
✅ Built-in version history
✅ Team folder sharing
✅ Automatic backup
✅ Mobile access
```

---

## 🔄 Sync Strategies

### Strategy 1: Cloud-First (Recommended)
**Drive is the source of truth, local is cache**

```
1. User edits file in Taminator
2. File saved to Drive immediately
3. Local cache updated
4. Other devices auto-sync within seconds
```

**Pros:**
- ✅ Always synced
- ✅ Never lose data
- ✅ Works on any device

**Cons:**
- ⚠️ Requires internet
- ⚠️ Slightly slower writes

### Strategy 2: Hybrid (Offline-First)
**Local is primary, sync to Drive periodically**

```
1. User edits file in Taminator
2. File saved locally first (fast!)
3. Background sync to Drive every 5 minutes
4. Conflict resolution on next sync
```

**Pros:**
- ✅ Works offline
- ✅ Fast writes
- ✅ Good for field work

**Cons:**
- ⚠️ Potential conflicts
- ⚠️ Delayed sync

### Strategy 3: Manual Sync
**User triggers sync manually**

```
1. User works offline all day
2. Clicks "Sync to Drive" when online
3. All changes uploaded at once
```

**Pros:**
- ✅ Full offline support
- ✅ User control

**Cons:**
- ❌ Easy to forget
- ❌ Risk of data loss

**Recommended**: Start with Cloud-First, add Hybrid later for offline support.

---

## 📊 Data Storage Layout

### Customer Data
```
Drive://Taminator/customers/
├── {customer-id}/
│   ├── customer.yaml          # Customer config
│   ├── reports/
│   │   ├── 2025-10-report.md
│   │   ├── 2025-09-report.md
│   │   └── 2025-08-report.md
│   ├── notes/
│   │   └── meeting-notes.md
│   ├── attachments/
│   │   └── architecture.pdf
│   └── archive/
│       └── old-reports/
```

### Settings (Cross-Device)
```
Drive://Taminator/settings/
├── settings.json              # User preferences (synced!)
├── themes/
│   └── custom-theme.json
└── keybindings.json
```

### Templates (Shared)
```
Drive://Taminator/templates/
├── report-templates/
│   ├── monthly-summary.md
│   ├── executive-brief.md
│   └── technical-deep-dive.md
└── email-templates/
    └── weekly-update.txt
```

---

## 🔐 Security & Permissions

### File Permissions

**Private by Default:**
- User's Taminator folder is private
- Only accessible with user's Google account
- Encrypted at rest by Google

**Team Sharing (Optional):**
```python
# Share customer folder with another TAM
drive.share_folder(
    folder_path="customers/td-bank",
    email="colleague@redhat.com",
    role="reader"  # or "writer"
)
```

**Team Folders:**
```
Drive://Taminator-Team/          # Shared team folder
├── customers/
│   └── shared-accounts/
├── templates/                   # Team report templates
└── playbooks/                   # Best practices
```

---

## 🚀 Migration Path

### Phase 1: Initialize Drive Structure
```bash
# API call or GUI button
POST /api/drive/initialize

Creates:
- Taminator/
- Taminator/customers/
- Taminator/settings/
- Taminator/templates/
```

### Phase 2: One-Time Migration
```bash
# Upload existing local data to Drive
POST /api/drive/sync/local-to-drive

Uploads:
- ~/Documents/rh/* → Drive://Taminator/customers/*
- ~/.config/taminator/* → Drive://Taminator/settings/*
```

### Phase 3: Switch to Cloud-First
```python
# Update CustomerService to use Drive backend
customer_service = CustomerService(
    storage_backend="drive"  # instead of "filesystem"
)
```

### Phase 4: Cleanup Local (Optional)
```bash
# Keep local as cache, or delete
rm -rf ~/Documents/rh/
# Data still safe in Drive!
```

---

## 📋 API Endpoints

### Drive Management
```bash
GET  /api/drive/status              # Check Drive integration status
POST /api/drive/initialize          # Create folder structure
GET  /api/drive/quota               # Get storage quota
GET  /api/drive/list?path=customers # List files
```

### File Operations
```bash
POST   /api/drive/upload            # Upload file
GET    /api/drive/download/{path}   # Download file
DELETE /api/drive/delete/{path}     # Delete file
```

### Sync Operations
```bash
POST /api/drive/sync/local-to-drive  # Upload local → Drive
POST /api/drive/sync/drive-to-local  # Download Drive → local
POST /api/drive/sync/auto            # Enable auto-sync
```

---

## 🎨 GUI Integration

### Settings Page
```
╔═══════════════════════════════════════════════════════════╗
║  Storage Settings                                        ║
╠═══════════════════════════════════════════════════════════╣
║  Storage Backend:                                        ║
║    ⚪ Local Filesystem                                    ║
║    🔵 Google Drive (Unlimited)                            ║
║                                                           ║
║  Drive Status: ✅ Connected                               ║
║  Storage Used: 127 MB / Unlimited                        ║
║  Last Sync: 2 minutes ago                                ║
║                                                           ║
║  [📤 Upload Local to Drive]  [📥 Download from Drive]    ║
║                                                           ║
║  Auto-Sync: [✅ Enabled]   Interval: [5 minutes ▼]       ║
╚═══════════════════════════════════════════════════════════╝
```

### Dashboard Sync Indicator
```
┌──────────────────────────────────────────┐
│  TD Bank                                 │
│  Last synced: 30 seconds ago ✅          │
│  [🔄 Sync Now]                           │
└──────────────────────────────────────────┘
```

---

## 🧪 Usage Examples

### Initialize Drive Storage
```python
from taminator.core.drive_storage import get_drive_storage

drive = get_drive_storage()

# Create folder structure
drive.initialize_structure()
```

### Upload Customer Data
```python
# Upload single file
drive.upload_file(
    local_path=Path("~/Documents/rh/td-bank/customer.yaml"),
    drive_path="customers/td-bank/customer.yaml"
)

# Upload entire local directory
drive.sync_from_local()
```

### Download Customer Data
```python
# Download single file
content = drive.download_file("customers/td-bank/customer.yaml")

# Download entire Drive to local
drive.sync_to_local()
```

### List Files
```python
# List customers
customers = drive.list_files("customers")

# List reports for customer
reports = drive.list_files("customers/td-bank/reports")
```

---

## ⚡ Performance Optimizations

### Local Cache
```python
# Fast reads from local cache
drive = DriveStorageManager(use_cache=True)

# First read: Downloads from Drive (slow)
content = drive.download_file("customers/td-bank/customer.yaml")

# Second read: Reads from cache (fast!)
content = drive.download_file("customers/td-bank/customer.yaml")
```

### Batch Operations
```python
# Upload multiple files at once
files = [
    ("customer.yaml", "customers/td-bank/customer.yaml"),
    ("report.md", "customers/td-bank/reports/2025-10.md"),
]

for local, drive_path in files:
    drive.upload_file(local, drive_path)
```

### Background Sync
```python
# Non-blocking sync
from fastapi import BackgroundTasks

def sync_in_background(background_tasks: BackgroundTasks):
    background_tasks.add_task(drive.sync_from_local)
```

---

## 🎯 Benefits Summary

### For Users
- ✅ **Never lose data** - Auto-backup to Drive
- ✅ **Access anywhere** - Any device, any location
- ✅ **No manual sync** - Automatic across devices
- ✅ **Mobile access** - View/edit on phone
- ✅ **Version history** - Undo mistakes easily
- ✅ **Team collaboration** - Share folders with colleagues

### For Developers
- ✅ **Unlimited storage** - No disk space limits
- ✅ **Built-in versioning** - Drive tracks changes
- ✅ **No backup code** - Drive handles it
- ✅ **Team features** - Sharing built-in
- ✅ **Mobile SDK** - Future mobile app easier

### For Red Hat
- ✅ **Cost savings** - Use existing Workspace license
- ✅ **Compliance** - Google Workspace is approved
- ✅ **Data sovereignty** - Control via Workspace admin
- ✅ **Enterprise features** - DLP, retention policies

---

## 🔮 Future Enhancements

### Phase 1 (v2.0)
- ✅ Drive backend implementation
- ✅ Manual sync (upload/download)
- ✅ Local cache for speed

### Phase 2 (v2.1)
- [ ] Auto-sync every N minutes
- [ ] Conflict resolution UI
- [ ] Offline mode support

### Phase 3 (v2.2)
- [ ] Team folder sharing
- [ ] Real-time collaboration
- [ ] Mobile app (Drive SDK)

### Phase 4 (v2.3)
- [ ] Drive search integration
- [ ] Google Docs integration (reports as Docs)
- [ ] Shared templates library

---

*Google Drive Storage Architecture for Taminator v2.0*  
*Unlimited cloud storage with automatic multi-device sync*

