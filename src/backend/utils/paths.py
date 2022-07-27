from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = SRC_DIR / 'backend'
APP_DIR = BACKEND_DIR / 'app'
CORE_DIR = BACKEND_DIR / 'core'
UTILS_DIR = BACKEND_DIR / 'utils'
ASSETS_DIR = BACKEND_DIR / 'assets'
MASKS_DIR = ASSETS_DIR / 'masks'