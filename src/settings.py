import sys
from os.path import join, dirname
from dotenv import load_dotenv
from pyaml_env import parse_config
from logging import basicConfig, INFO

basicConfig(
    stream=sys.stdout,
    level=INFO,
    format="[%(asctime)s] {%(filename)s:%(lineno)d} %(name)s %(levelname)s - %(message)s",
)

dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)

app_config_path = join(dirname(__file__), "app_config.yaml")
app_config = parse_config(app_config_path)