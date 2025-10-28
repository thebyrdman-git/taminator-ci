"""
Diagnostics and Log Collection API
Generate debug packages for GitLab issue reporting
"""

from fastapi import APIRouter, Response
from fastapi.responses import FileResponse
import logging
import tarfile
import tempfile
from pathlib import Path
from datetime import datetime
import platform
import json
import subprocess

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/diagnostics", tags=["diagnostics"])


def collect_system_info() -> dict:
    """Collect system information for diagnostics"""
    info = {
        "timestamp": datetime.now().isoformat(),
        "taminator_version": "2.0.0",
        "system": {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "python_version": platform.python_version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        }
    }
    
    # Check rhcase
    try:
        from ...services.rhcase_service import RhcaseService
        rhcase = RhcaseService()
        info["rhcase"] = rhcase.get_info()
    except Exception as e:
        info["rhcase"] = {"error": str(e)}
    
    # Check VPN (basic ping test)
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", "issues.redhat.com"],
            capture_output=True,
            timeout=5
        )
        info["network"] = {
            "vpn_reachable": result.returncode == 0,
            "issues_redhat_com": "reachable" if result.returncode == 0 else "unreachable"
        }
    except Exception as e:
        info["network"] = {"error": str(e)}
    
    return info


def collect_logs(log_dir: Path, lines: int = 1000) -> str:
    """Collect recent logs from log files"""
    logs = []
    
    log_files = [
        "taminator.log",
        "api.log", 
        "service.log"
    ]
    
    for log_file in log_files:
        log_path = log_dir / log_file
        if log_path.exists():
            try:
                with open(log_path, 'r') as f:
                    # Get last N lines
                    all_lines = f.readlines()
                    recent_lines = all_lines[-lines:]
                    logs.append(f"\n{'='*60}\n")
                    logs.append(f"LOG FILE: {log_file}\n")
                    logs.append(f"{'='*60}\n")
                    logs.extend(recent_lines)
            except Exception as e:
                logs.append(f"\nERROR reading {log_file}: {e}\n")
    
    return "".join(logs)


@router.post("/collect")
async def collect_diagnostics(lines: int = 1000):
    """
    Collect diagnostics package for GitLab issue reporting
    
    Creates a tar.gz with:
    - System information
    - Recent log files
    - Debug settings
    - Service health status
    
    Args:
        lines: Number of recent log lines to include (default: 1000)
    
    Returns:
        Tarball ready to attach to GitLab issue
    """
    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg_dir = Path(tmpdir) / "taminator-diagnostics"
            pkg_dir.mkdir()
            
            # 1. System info
            system_info = collect_system_info()
            with open(pkg_dir / "system-info.json", 'w') as f:
                json.dump(system_info, f, indent=2)
            
            # 2. Collect logs
            log_dir = Path.home() / ".local" / "state" / "taminator" / "log"
            if log_dir.exists():
                logs_content = collect_logs(log_dir, lines=lines)
                with open(pkg_dir / "logs.txt", 'w') as f:
                    f.write(logs_content)
            
            # 3. Debug settings
            debug_settings_file = Path.home() / ".config" / "taminator" / "debug_settings.json"
            if debug_settings_file.exists():
                with open(debug_settings_file, 'r') as src:
                    with open(pkg_dir / "debug-settings.json", 'w') as dst:
                        dst.write(src.read())
            
            # 4. Create README for the package
            readme = f"""# Taminator Diagnostics Package

**Generated**: {datetime.now().isoformat()}
**Taminator Version**: 2.0.0
**System**: {platform.system()} {platform.version()}

## Contents

- `system-info.json` - System and component information
- `logs.txt` - Recent log files (last {lines} lines)
- `debug-settings.json` - Debug logging configuration

## How to Attach to GitLab Issue

1. Go to: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
2. Click "New Issue"
3. Fill in title and description
4. Drag this file to attach
5. Submit

## Privacy Note

This package contains:
- System information (OS, Python version)
- Application logs (may contain case numbers, customer names)
- No passwords or API tokens

**Review logs.txt before sharing if concerned about sensitive data.**
"""
            with open(pkg_dir / "README.txt", 'w') as f:
                f.write(readme)
            
            # 5. Create tarball
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            tarball_name = f"taminator-diagnostics-{timestamp}.tar.gz"
            tarball_path = Path(tmpdir) / tarball_name
            
            with tarfile.open(tarball_path, "w:gz") as tar:
                tar.add(pkg_dir, arcname="taminator-diagnostics")
            
            logger.info(f"📦 Diagnostics package created: {tarball_name}")
            
            # Return file
            return FileResponse(
                path=str(tarball_path),
                filename=tarball_name,
                media_type="application/gzip",
                headers={
                    "Content-Disposition": f"attachment; filename={tarball_name}"
                }
            )
    
    except Exception as e:
        logger.error(f"❌ Failed to collect diagnostics: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/info")
async def diagnostics_info():
    """
    Get diagnostic information (without creating package)
    
    Returns:
        System info and health status
    """
    try:
        system_info = collect_system_info()
        
        # Add log file info
        log_dir = Path.home() / ".local" / "state" / "taminator" / "log"
        log_files = []
        if log_dir.exists():
            for log_file in log_dir.glob("*.log"):
                stat = log_file.stat()
                log_files.append({
                    "name": log_file.name,
                    "size_mb": round(stat.st_size / 1024 / 1024, 2),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        system_info["log_files"] = log_files
        
        return {
            "success": True,
            "info": system_info
        }
    
    except Exception as e:
        logger.error(f"❌ Failed to get diagnostics info: {e}")
        return {
            "success": False,
            "error": str(e)
        }

