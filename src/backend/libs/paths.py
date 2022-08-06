from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = SRC_DIR / 'backend'
APP_DIR = BACKEND_DIR / 'app'
MODULES_DIR = BACKEND_DIR / 'modules'
LIBS_DIR = BACKEND_DIR / 'libs'
ASSETS_DIR = BACKEND_DIR / 'assets'
MASKS_DIR = ASSETS_DIR / 'masks'
STORAGE_DIR = BACKEND_DIR / 'storage'

DB_CONN_STR = f"sqlite:///{str(STORAGE_DIR)}/face.db"