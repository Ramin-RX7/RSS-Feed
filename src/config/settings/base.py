from pathlib import Path

import environ


__all__ = ("BASE_ENV", "BASE_DIR", "BASE_URL","SECRET_KEY", "DEBUG")



BASE_ENV = environ.Env()
environ.Env.read_env('.env')

BASE_URL = BASE_ENV("URL")

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = BASE_ENV("SECRET_KEY")

DEBUG = BASE_ENV.bool("DEBUG")
