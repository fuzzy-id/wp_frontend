import datetime
from sqlalchemy import Column, Integer, Enum, Sequence, DateTime, String
from wp_frontend.models import Base, map_to_beautifull_names

setable = ['temp_einsatz',
           'temp_BasisSoll',
           'hzg_KlSteilheit',
           'hzg_Hysterese',
           'hzg_PumpenNachl',
           'ww_Abschaltung',
           'ww_TempSoll',
           'ww_Hysterese',
           'uhrzeit',
           'datum',
           'handabschaltung']

attribute_enum = [ map_to_beautifull_names[s] for s in setable ]

class DataToSet(Base):
    __tablename__ = 'wp_setdata'
    id = Column(Integer, Sequence('set_data_id'),
                primary_key=True)
    datetime = Column(DateTime())
    user = Column(String(16))
    oldval = Column(String(16))
    newval = Column(String(16))
    status = Column(Enum('pending', 'success', 
                         'fail', 'outdated'))
    WPsetVal_output = Column(String(255), default='')
    attribute = Column(Enum(*attribute_enum))

    def __init__(self, user, attribute, newval, oldval ):
        self.user = user
        self.oldval = oldval
        self.newval = newval
        self.attribute = attribute
        self.status = 'pending'
        self.datetime = datetime.datetime.now()

    @classmethod
    def get_latest(cls, session, number):
        columns = (cls.datetime, cls.user, cls.attribute, cls.oldval,
                   cls.newval, cls.status, cls.WPsetVal_output, )
        query = session.query(*columns)
        query = query.order_by(cls.id.desc())
        query = query.limit(number)

        return query.all()
