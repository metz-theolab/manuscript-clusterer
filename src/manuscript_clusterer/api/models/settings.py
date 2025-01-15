"""Settings file for the API.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the API.
    """
    db_host: str = "localhost"
    db_port: int = 27017
    db_name: str = "manuscriptsDB"