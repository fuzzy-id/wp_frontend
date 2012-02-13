# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Sequence, String, Text

from wp_frontend.models import Base

class BackupTemplate(Base):

    __tablename__ = 'backup_template'
    id = Column(Integer, Sequence('template_id'), primary_key=True)
    name = Column(String(20))
    root = Column(String(40))
    exclude = Column(Text)
