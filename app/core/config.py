from pydantic import field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

def validate_not_default(value: str) -> str:
    if not value or value.strip() == "" or value.lower() == "changethis":
        raise ValueError(
            "Value is missing or set to default 'changethis', please change it."
        )
    return value

class Settings(BaseSettings):

    DB_TYPE: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_PORT: int

    GEMINI_API_KEY: str
    GEMINI_MODEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    @field_validator("*", mode="before")
    def validate_all_str_fields(cls, value, info):
        field_type = cls.model_fields[info.field_name].annotation
        if field_type is str:
            return validate_not_default(value)
        return value

try:
    settings = Settings() # type: ignore[call-arg]
except ValidationError as e:
    raise
