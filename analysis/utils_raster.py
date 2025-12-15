"""
Shared raster utility functions
Used across solar, wind, and hydro suitability workflows
"""

from pathlib import Path
import datetime


def log_step(message: str):
    """Print timestamped log messages"""
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {message}")


def ensure_exists(path):
    """Ensure a file exists"""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"❌ Missing file: {path}")
    return path


def ensure_folder(path):
    """Create folder if it doesn't exist"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def check_file_exists(path):
    """
    Check if a file exists and raise a clear error if not.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"❌ Missing file: {path}")
    return path





"""
utils_raster.py
----------------
Reusable raster utility functions for renewable energy suitability analysis.

Used by:
- solar_suitability.py
- wind_suitability.py
- hydro_suitability.py

Environment:
- QGIS Python Console OR
- Python with GDAL installed
"""

from pathlib import Path

def log_step(message):
    """
    Simple logger for workflow steps.
    """
    print(f"🟢 {message}")


def placeholder_raster_alignment():
    """
    Placeholder for raster alignment logic.

    Future steps:
    - Reproject to EPSG:4326
    - Match resolution
    - Match extent to reference raster
    """
    log_step("Raster alignment placeholder – logic to be implemented")


def placeholder_masking():
    """
    Placeholder for raster masking using landmask or AOI.
    """
    log_step("Raster masking placeholder – logic to be implemented")
