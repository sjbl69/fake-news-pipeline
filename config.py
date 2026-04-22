import os
from dotenv import load_dotenv

load_dotenv()

def get_optional_env(var_name: str):
    return os.getenv(var_name)