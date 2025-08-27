# =============================================
# app/repositories/project_repository.py
# =============================================
class ProjectRepository(ARepository[Project]):
    def _build(self, data: Dict[str, Any]) -> Project:
        return Project.from_dict(data)