from __future__ import annotations
from typing import Any, Dict, Mapping, Tuple, Optional, List
import re
import json

_param_rx = re.compile(r":([a-zA-Z_]\w*)")

def is_mariadb_engine(engine) -> bool:
    return "mariadb" in (type(engine).__module__ or "").lower()

def adapt_params_for_engine(engine, sql: str, params: Optional[Mapping[str, Any]]) -> Tuple[str, Optional[List[Any]] | Dict[str, Any]]:
    """
    For MariaDB (mariadb connector), convert :named placeholders to '?' and return
    a positional list of values in order of appearance. For non-MariaDB, return
    the original SQL and a plain dict.
    """
    if params is None:
        return sql, None

    if is_mariadb_engine(engine):
        # Find names in order of appearance and replace with '?'
        names = _param_rx.findall(sql)
        sql_qmark = _param_rx.sub("?", sql)
        # Build a positional list aligned to those names
        seq = [params[n] if n in params else None for n in names]
        return sql_qmark, seq

    # Default: keep named placeholders and pass a real dict with string keys
    return sql, {str(k): v for k, v in dict(params).items()}

def roles_set(ctx) -> set[str]:
    raw = getattr(ctx, "roles", []) or []
    if isinstance(raw, str):
        raw = [raw]
    return {str(r).strip().lower() for r in raw if str(r).strip()}

def dumps_json(val: Any) -> Any:
    if val is None:
        return None
    return json.dumps(val, separators=(",", ":"), ensure_ascii=False)

def loads_json(val: Any) -> Any:
    if val is None:
        return None
    if isinstance(val, (dict, list)):
        return val
    try:
        return json.loads(val)
    except Exception:
        return val
