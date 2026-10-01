from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.db import get_db
from app.services.project_service import create_project, get_projects


router = APIRouter(prefix="/projects", tags=["Projects"])


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


@router.post("/")
def create(
    project: ProjectCreate,
    db: Session = Depends(get_db),
):
    return create_project(
        db=db,
        name=project.name,
        description=project.description,
    )


@router.get("/")
def list_projects(
    db: Session = Depends(get_db),
):
    return get_projects(db)
