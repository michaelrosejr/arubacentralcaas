import yaml
from pydantic import BaseSettings


class Settings(BaseSettings):
    ACCOUNT: str = "central_info"


settings = Settings()  # type: ignore

with open(r"config/config.yaml") as file:
    configfile = yaml.load(file, Loader=yaml.FullLoader)
