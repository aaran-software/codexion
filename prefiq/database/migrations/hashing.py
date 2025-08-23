# prefiq/database/migrations/hashing.py
import hashlib
import inspect
from textwrap import dedent

def compute_file_hash(file_path: str) -> str:
    """
    Compute SHA256 hash of the file content.
    """
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_callable_hash(fn) -> str:
    """
    Compute a stable SHA256 hash for a callable's implementation.
    Prefers hashing the source of the callable (dedented & stripped).
    Falls back to file-hash, then to code object attributes if source is unavailable.
    """
    # 1) Try to unwrap decorators and grab source
    try:
        target = inspect.unwrap(fn)
    except Exception:
        target = fn

    try:
        src = inspect.getsource(target)
        norm = dedent(src).strip()
        return hashlib.sha256(norm.encode("utf-8")).hexdigest()
    except (OSError, TypeError):  # builtins, C-extensions, or no source
        pass

    # 2) Fallback: hash containing file if resolvable
    try:
        mod = inspect.getmodule(target)
        file_path = getattr(mod, "__file__", None)
        if file_path:
            return compute_file_hash(file_path)
    except Exception:
        pass

    # 3) Last-resort: hash code object signature
    h = hashlib.sha256()
    co = getattr(target, "__code__", None)
    payload = (
        getattr(target, "__qualname__", repr(target)),
        getattr(co, "co_code", b""),
        getattr(co, "co_consts", ()),
        getattr(co, "co_names", ()),
        getattr(co, "co_varnames", ()),
    )
    for part in payload:
        if isinstance(part, bytes):
            h.update(part)
        else:
            h.update(str(part).encode("utf-8", "ignore"))
    return h.hexdigest()
