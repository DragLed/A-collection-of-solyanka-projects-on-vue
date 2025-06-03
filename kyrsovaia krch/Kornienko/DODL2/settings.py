from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASS: str
    DATABASE_NAME: str

    @property
    def db_url_sync(self):
        return (f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASS}"
                f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}")
    model_config =  SettingsConfigDict(env_file=".env")

settings = Settings()

