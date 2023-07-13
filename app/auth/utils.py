from ..extensions import db


def init_and_commit(cls, attributes):
    instance = cls(**attributes)
    db.session.add(instance)
    db.session.commit()
