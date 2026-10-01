from sqlalchemy.orm import Session

from app.database.models import Project


def create_project(
    db: Session,
    name: str,
    description: str | None = None,
):
    project = Project(
        name=name,
        description=description,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_projects(db: Session):
    return db.query(Project).all()
