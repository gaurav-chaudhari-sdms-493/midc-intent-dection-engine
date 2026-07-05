from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def _create(self, db: Session, obj: ModelType):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def _get(self, db: Session, obj_id):
        return db.get(self.model, obj_id)

    def _get_all(self, db: Session):
        return db.query(self.model).all()



    def _delete(self, db: Session, obj):
        db.delete(obj)
        db.commit()
