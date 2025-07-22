Great — we’ll enhance your config manager to support:

---

### ✅ Features:

1. ✅ **Nested config paths** (`docker.compose`, `app.settings`)
2. ✅ **Auto-validation** of config structure (using Pydantic models)
3. ✅ Config fallback to default if file is missing or invalid

---

## 🔧 Step-by-Step Setup

### 1. ✅ Create `prefiq/config/models.py` (Config Schemas)

```python
from typing import List, Dict, Union
from pydantic import BaseModel, Field


class ComposeEntry(BaseModel):
    service_name: str  # e.g., sundar_com
    path: str          # e.g., E:/Workspace/codexion/docker/docker-compose-sundar_com.yml
    port: Union[int, str]


class DockerConfig(BaseModel):
    COMPOSE_FILE: List[ComposeEntry]
    DOCKERFILE_NAME: str
    DOCKERFILE_PATH: List[str]
```

> You can reuse this for validation before saving or reading.

---

### 2. ✅ Update `prefiq/config/manager.py`

```python
import json
from pathlib import Path
from typing import Any, Optional, Type, TypeVar, Union
from pydantic import BaseModel, ValidationError

from prefiq import CPATH
from prefiq.utils.cprint import cprint_error

T = TypeVar("T", bound=BaseModel)

CONFIG_DIR = CPATH.CONFIG_DIR


def _get_config_path(name: str) -> Path:
    """Support nested config like docker.compose → config/docker/compose.json"""
    path_parts = name.split(".")
    return CONFIG_DIR.joinpath(*path_parts).with_suffix(".json")


def config_load(name: str, schema: Optional[Type[T]] = None) -> Union[dict, T]:
    path = _get_config_path(name)
    if not path.exists():
        return schema() if schema else {}
    try:
        with path.open("r") as f:
            data = json.load(f)
            if schema:
                return schema.parse_obj(data)
            return data
    except (json.JSONDecodeError, ValidationError) as e:
        cprint_error(f"[err] Invalid config in '{path}': {str(e)}")
        return schema() if schema else {}


def config_save(name: str, data: Union[dict, BaseModel]):
    path = _get_config_path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        if isinstance(data, BaseModel):
            json.dump(data.dict(), f, indent=2)
        else:
            json.dump(data, f, indent=2)


# ---- Specific helpers ---- #

from prefiq.config.models import DockerConfig


def config_get_docker() -> DockerConfig:
    return config_load("docker.compose", DockerConfig)


def config_set_docker(data: DockerConfig):
    config_save("docker.compose", data)
```

---

### 3. ✅ Usage Example

```python
from prefiq.config.manager import config_get_docker, config_set_docker
from prefiq.config.models import DockerConfig, ComposeEntry

# Get and print
docker_conf = config_get_docker()
print(docker_conf.DOCKERFILE_NAME)

# Modify and save
docker_conf.COMPOSE_FILE.append(
    ComposeEntry(service_name="new_app", path="E:/Workspace/docker/new.yml", port=5050)
)
config_set_docker(docker_conf)
```

---

## 🧠 Benefits of This Design

✅ Cleaner structure
✅ Strong schema validation (no bad data in configs)
✅ Nested JSON files like:

```
config/docker/compose.json
config/app/settings.json
```

---

Would you like this to support defaults or auto-merge schema when missing fields?
