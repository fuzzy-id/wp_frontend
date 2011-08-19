import datetime
from sqlalchemy import Column, Integer, Enum, Sequence, DateTime, String
from wp_frontend.models import Base


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
    WPsetVal_output = Column(String(255))
    attribute = Column(Enum('Hzg:TempEinsatz', 
                            'Hzg:TempBasisSoll',
                            'Hzg:KlSteilheit', 
                            'Hzg:Hysterese',
                            'Hzg:PumpenNachl', 
                            'Ww:Abschaltung',
                            'Ww:Temp-Soll', 'Ww:Hysterese',
                            'Handabschaltung', 'Uhrzeit',
                            'Datum'))

    def __init__(self, user, attribute, newval ):
        self.user = user
        self.oldval = ""
        self.newval = newval
        self.attribute = attribute
        self.status = 'pending'
        self.datetime = datetime.datetime.now()
