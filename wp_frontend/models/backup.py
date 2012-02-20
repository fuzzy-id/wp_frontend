# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Sequence, String, Text

from wp_frontend.models import Base

class BackupTemplate(Base):

    __tablename__ = 'backup_template'
    ident = Column(Integer, Sequence('template_id'), primary_key=True)
    name = Column(String(20), unique=True)
    root = Column(String(40))
    excludes = Column(Text)

    def __init__(self, name, root, excludes, ident=None):
        self.name = name
        self.root = root
        self.excludes = excludes
        if ident is not None:
            self.ident = ident

    @classmethod
    def get_template_names(cls, session):
        query = session.query(cls.name)
        query = query.order_by(cls.ident.desc())
        result = query.all()
        result = [ res[0] for res in result ]
        return tuple(result)

    @classmethod
    def get_template_by_name(cls, session, name):
        query = session.query(cls)
        query = query.filter(cls.name == name)
        result = query.all()
        assert len(result) == 1
        return result[0]
