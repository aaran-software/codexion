# =============================================
# app/services/project_service.py
# =============================================
class ProjectService(AService[Project]):
    def before_create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Example: ensure slug exists and is lowercase
        slug = data.get("slug") or data.get("name", "").strip().lower().replace(" ", "-")
        data["slug"] = slug
        data.setdefault("meta", {})
        return data