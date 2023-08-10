from pathlib import Path

import yaml

yamlPath = Path(__file__).with_name("env_config.yaml")
f = open(yamlPath, "r", encoding="utf-8")
cfg = f.read()
f.close()

env_config = yaml.safe_load(cfg)
REDIS_HOST = env_config["redis"]["host"]
REDIS_PORT = env_config["redis"]["port"]
REDIS_DB = env_config["redis"]["db"]
REDIS_PWD = env_config["redis"]["password"]

