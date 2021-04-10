from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")
HOST = env("HOST")

DB_HOST = env("DB_HOST")
DB_NAME = env("DB_NAME")
DB_USER = env("DB_USER")
DB_PASSWORD = env("DB_PASSWORD")
