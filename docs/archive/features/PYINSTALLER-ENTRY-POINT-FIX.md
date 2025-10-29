# PyInstaller Entry Point Fix

**Date:** October 28, 2025, 4:35 PM  
**Issue:** Service binary failing with `ImportError: attempted relative import with no known parent package`

---

## 🐛 Problem

**Error:**
```
Traceback (most recent call last):
  File "main.py", line 17, in <module>
ImportError: attempted relative import with no known parent package
```

**Root Cause:**
- PyInstaller spec was using `src/taminator/api/main.py` as entry point
- `main.py` uses relative imports (`from ..core.exceptions import ...`)
- Relative imports don't work in PyInstaller-packaged binaries without proper package structure

---

## ✅ Solution

**Changed entry point from:**
```python
# OLD - Wrong entry point
Analysis(
    ['src/taminator/api/main.py'],  # ❌ Has relative imports
    ...
)
```

**To:**
```python
# NEW - Correct entry point
Analysis(
    ['src/taminator/cli_service.py'],  # ✅ No relative imports
    ...
)
```

**Why `cli_service.py` works:**
1. Uses only standard library imports (no relative imports)
2. Loads FastAPI app via string reference: `"taminator.api.main:app"`
3. Proper `if __name__ == "__main__"` structure
4. This is the intended entry point for the service

**Added hiddenimports:**
- All taminator modules explicitly listed
- Ensures PyInstaller includes all needed code
- Routes, services, core modules all specified

---

## 🔧 Files Modified

1. **`taminator-service.spec`**
   - Changed entry point to `cli_service.py`
   - Added comprehensive hiddenimports list

2. **Ansible playbooks** (automatic)
   - `build-taminator-rocky.yml` uses updated spec
   - Rebuild triggered automatically

---

## 🧪 Testing

**Fixed AppImage deployed to:**
- Local: `/home/jbyrd/TAMINATOR/gui/dist/Taminator-2.0.0-rocky.AppImage`
- VM: `/home/testuser/taminator-test/Taminator-2.0.0.AppImage`

**Test command:**
```bash
ssh -X testuser@192.168.122.100
cd /home/testuser/taminator-test
./Taminator-2.0.0.AppImage --no-sandbox
```

**Expected result:**
- Service starts successfully
- No import errors
- Status bar shows "Service: Running"

---

## 📚 Lessons Learned

1. **Always use the intended entry point**
   - Don't point PyInstaller at internal modules
   - Use the CLI entry point designed for external execution

2. **Relative imports break in packaged apps**
   - PyInstaller can't always resolve relative imports
   - Use absolute imports or string references

3. **Test the binary early**
   - We saw this error in build logs but ignored it
   - Should have caught it immediately

4. **hiddenimports are critical**
   - Dynamic imports (like uvicorn's string loading) need explicit hiddenimports
   - Better to over-specify than under-specify

---

## ✅ Status

**FIXED** - Rebuilt and ready for testing

---

*Fixed: October 28, 2025, 4:35 PM*

