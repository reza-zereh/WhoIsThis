import os
import shutil
import time
from pathlib import Path
import uuid
import dotenv

from libs import paths

def remove_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def remove_folder_contents(directory_path, delay=0):
    time.sleep(delay)
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    p = Path(directory_path)
    p.mkdir(parents=True)


def remove_folder(directory_path):
    shutil.rmtree(directory_path)


def unique_id():
    return uuid.uuid1().hex


def load_env():
    if not os.path.exists(paths.DOTENV_FP):
        print(
            "\nError: No .env file found! Please rename "
            "'.env.sample' to '.env' and provide required information in it."
        )
        exit()
    dotenv.load_dotenv(str(paths.DOTENV_FP))