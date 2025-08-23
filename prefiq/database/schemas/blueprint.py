# prefiq/database/schemas/blueprint.py

# Runtime driver resolution happens in builder.create(). This shim only exists
# for type annotations like:  def schema(t: bp.TableBlueprint): ...
# Do NOT bind a concrete class here to avoid locking the driver at import time.

class TableBlueprint:  # typing placeholder
    pass

__all__ = ["TableBlueprint"]

