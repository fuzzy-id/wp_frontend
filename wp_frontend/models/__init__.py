import transaction
from pyramid.security import Allow, Everyone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension


class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'login'),
                (Allow, 'group:users', 'user') ]

    def __init__(self, request):
        pass

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
