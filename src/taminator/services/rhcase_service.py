"""
RHCase Service
Manages execution of rhcase commands and analysis
"""

import subprocess
import shutil
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class RhcaseService:
    """Service for executing rhcase commands"""
    
    def __init__(self):
        """Initialize rhcase service"""
        self.rhcase_path = self._find_rhcase()
        if self.rhcase_path:
            version = self.get_version()
            logger.info(f"🤖 RhcaseService initialized (path: {self.rhcase_path}, version: {version})")
        else:
            logger.warning("⚠️  rhcase not found - functionality will be limited")
    
    def _find_rhcase(self) -> Optional[str]:
        """
        Find rhcase executable (bundled first, then system PATH)
        
        Priority:
        1. Bundled rhcase in Taminator package
        2. System PATH
        
        Returns:
            Path to rhcase executable or None if not found
        """
        # Priority 1: Bundled rhcase (in AppImage or dev)
        bundled_locations = [
            # Production AppImage
            Path(__file__).parent.parent.parent / "bin" / "rhcase",
            # Development mode
            Path(__file__).parent.parent.parent.parent / "bin" / "rhcase",
            # Alternative packaging location
            Path(__file__).parent.parent / "resources" / "bin" / "rhcase"
        ]
        
        for bundled_path in bundled_locations:
            if bundled_path.exists() and bundled_path.is_file():
                logger.info(f"✅ Found bundled rhcase at: {bundled_path}")
                return str(bundled_path)
        
        # Priority 2: System PATH
        system_rhcase = shutil.which('rhcase')
        if system_rhcase:
            logger.info(f"✅ Found system rhcase at: {system_rhcase}")
            return system_rhcase
        
        logger.warning("⚠️  rhcase not found (not bundled and not in PATH)")
        return None
    
    def is_available(self) -> bool:
        """
        Check if rhcase is available
        
        Returns:
            True if rhcase is installed and accessible
        """
        return self.rhcase_path is not None
    
    async def execute(
        self,
        command: str,
        timeout: int = 60
    ) -> Dict[str, Any]:
        """
        Execute rhcase command
        
        Args:
            command: Command to execute (e.g., "analyze 04056105")
            timeout: Command timeout in seconds (default: 60s)
            
        Returns:
            Dict with output, error, and exit code
            
        Raises:
            RuntimeError: If rhcase not available
        """
        if not self.is_available():
            raise RuntimeError(
                "rhcase command not found. "
                "Ensure rhcase is bundled with Taminator or install from: "
                "https://gitlab.cee.redhat.com/gvaughn/hatter-pai"
            )
        
        # Sanitize command (remove 'rhcase' prefix if included)
        clean_command = command.strip()
        if clean_command.startswith('rhcase '):
            clean_command = clean_command[7:]  # Remove 'rhcase ' prefix
        
        # Build full command
        full_command = [self.rhcase_path] + clean_command.split()
        
        logger.info(f"🤖 Executing: {' '.join(full_command)}")
        
        try:
            # Execute command
            process = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = process.stdout or ""
            error = process.stderr or ""
            exit_code = process.returncode
            
            # Log result
            if exit_code == 0:
                logger.info(f"✅ rhcase command succeeded (exit code: {exit_code})")
            else:
                logger.warning(f"⚠️  rhcase command failed (exit code: {exit_code})")
                if error:
                    logger.debug(f"stderr: {error}")
            
            return {
                "output": output,
                "error": error,
                "exit_code": exit_code,
                "success": exit_code == 0,
                "command": clean_command
            }
            
        except subprocess.TimeoutExpired:
            logger.error(f"❌ rhcase command timed out after {timeout}s")
            raise RuntimeError(f"Command timed out after {timeout} seconds")
        
        except Exception as e:
            logger.error(f"❌ rhcase execution error: {e}")
            raise RuntimeError(f"Failed to execute rhcase: {str(e)}")
    
    async def analyze_case(self, case_id: str) -> Dict[str, Any]:
        """
        Analyze a specific case
        
        Args:
            case_id: Case ID to analyze
            
        Returns:
            Analysis results
        """
        return await self.execute(f"analyze {case_id}")
    
    async def list_cases(self, account: Optional[str] = None) -> Dict[str, Any]:
        """
        List cases for account
        
        Args:
            account: Account name (optional)
            
        Returns:
            Case list
        """
        if account:
            return await self.execute(f"list {account}")
        else:
            return await self.execute("list")
    
    async def search_kcs(self, query: str) -> Dict[str, Any]:
        """
        Search KCS articles
        
        Args:
            query: Search query
            
        Returns:
            Search results
        """
        return await self.execute(f"kcs search {query}")
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check rhcase health (run doctor command)
        
        Returns:
            Health status
        """
        try:
            return await self.execute("doctor")
        except Exception as e:
            return {
                "output": "",
                "error": str(e),
                "exit_code": 1,
                "success": False,
                "command": "doctor"
            }
    
    def get_version(self) -> Optional[str]:
        """
        Get rhcase version
        
        Returns:
            Version string or None if unavailable
        """
        if not self.is_available():
            return None
        
        try:
            result = subprocess.run(
                [self.rhcase_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            # Note: rhcase --version returns exit code 1 (this is normal)
            version = result.stdout.strip() or result.stderr.strip()
            return version if version else "unknown"
        except Exception as e:
            logger.warning(f"Could not get rhcase version: {e}")
            return "unknown"
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get rhcase installation info
        
        Returns:
            Info about rhcase installation
        """
        return {
            "available": self.is_available(),
            "path": self.rhcase_path,
            "version": self.get_version() if self.is_available() else None,
            "bundled": self._is_bundled()
        }
    
    def _is_bundled(self) -> bool:
        """
        Check if using bundled rhcase (vs system PATH)
        
        Returns:
            True if using bundled version
        """
        if not self.rhcase_path:
            return False
        
        # Check if path contains Taminator package directories
        path_str = str(self.rhcase_path)
        return any(marker in path_str for marker in ['taminator', 'resources', 'bin'])
