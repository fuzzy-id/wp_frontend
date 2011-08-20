import time
import datetime
from sqlalchemy import Column, Float, Integer, Enum, Sequence, Date, Time, String, func
from wp_frontend.models import Base
from wp_frontend.models.column_calculator import ColumnCalculator

class PulledData(Base):
    __tablename__ = 'wp_data'
    id = Column(Integer, Sequence('data_id'), 
                primary_key=True)
    tsp = Column('tsp_0501_0500', Integer, default=0)
    version = Column('m_0000', Integer, default=0)
    datum_version = Column('m_0001', Date, default=datetime.date.min)
    betriebsmodus = Column('m_0002', String(8), default='')
    temp_aussen = Column('m_0100', Float, default=0.0)
    temp_aussen24 = Column('m_0101', Float, default=0.0)
    temp_aussen1 = Column('m_0102', Float, default=0.0)
    temp_RlSoll = Column('m_0103', Float, default=0.0)
    temp_Rl = Column('m_0104', Float, default=0.0)
    temp_Vl = Column('m_0105', Float, default=0.0)
    temp_WWSoll = Column('m_0106', Float, default=0.0)
    temp_WW = Column('m_0107', Float, default=0.0)
    temp_raum = Column('m_0108', Float, default=0.0)
    temp_raum1 = Column('m_0109', Float, default=0.0)
    temp_WQein = Column('m_0110', Float, default=0.0)
    temp_WQaus = Column('m_0111', Float, default=0.0)
    temp_Verdampfer = Column('m_0112', Float, default=0.0)
    temp_Kondensator = Column('m_0113', Float, default=0.0)
    temp_Saugleitung = Column('m_0114', Float, default=0.0)
    m_0115 = Column(Float, default=0.0)
    druck_Verdampfer = Column('m_0116', Float, default=0.0)
    druck_Kondensator = Column('m_0117', Float, default=0.0)
    m_0200 = Column(Enum('true','false','undef'), default='undef')
    temp_einsatz = Column('m_0201', Float, default=0.0)
    m_0202 = Column(Float, default=0.0)
    m_0203 = Column(Float, default=0.0)
    m_0204 = Column(Float, default=0.0)
    m_0205 = Column(Float, default=0.0)
    m_0206 = Column(Float, default=0.0)
    m_0207 = Column(Enum('true','false','undef'), default='undef')
    m_0208 = Column(Float, default=0.0)
    m_0209 = Column(Integer, default=0)
    m_0210 = Column(Float, default=0.0)
    m_0211 = Column(Time, default=datetime.time())
    m_0212 = Column(Time, default=datetime.time())
    m_0213 = Column(Time, default=datetime.time())
    m_0214 = Column(Time, default=datetime.time())
    m_0215 = Column(Float, default=0.0)
    m_0216 = Column(Float, default=0.0)
    m_0217 = Column(Integer, default=0)
    m_0300 = Column(Enum('true','false','undef'), default='undef')
    m_0301 = Column(Float, default=0.0)
    m_0302 = Column(Float, default=0.0)
    m_0303 = Column(Float, default=0.0)
    m_0304 = Column(Float, default=0.0)
    m_0305 = Column(Float, default=0.0)
    m_0306 = Column(Float, default=0.0)
    m_0400 = Column(Enum('true','false','undef'), default='undef')
    m_0401 = Column(Time, default=datetime.time())
    m_0402 = Column(Time, default=datetime.time())
    m_0403 = Column(Float, default=0.0)
    m_0404 = Column(Float, default=0.0)
    m_0405 = Column(Float, default=0.0)
    m_0406 = Column(Float, default=0.0)
    m_0407 = Column(Float, default=0.0)
    uhrzeit = Column('m_0500', Time, default=datetime.time())
    datum = Column('m_0501', Date, default=datetime.date.min)
    betriebsstunden = Column('m_0502', Float, default=0.0)
    m_0503 = Column(Float, default=0.0)
    m_0504 = Column(Float, default=0.0)
    m_0505 = Column(Float, default=0.0)
    m_0506 = Column(Time, default=datetime.time())
    m_0507 = Column(Date, default=datetime.date.min)
    m_0508 = Column(Time, default=datetime.time())
    m_0509 = Column(Date, default=datetime.date.min)
    m_0510 = Column(Enum('true','false','undef'), default='undef')
    m_0511 = Column(Enum('true','false','undef'), default='undef')
    m_0512 = Column(String(24))
    m_0600 = Column(Integer, default=0)
    m_0601 = Column(Enum('true','false','undef'), default='undef')
    m_0602 = Column(Enum('true','false','undef'), default='undef')
    m_0603 = Column(Enum('true','false','undef'), default='undef')
    m_0604 = Column(Enum('true','false','undef'), default='undef')
    m_0605 = Column(Integer, default=0)
    m_0606 = Column(Enum('true','false','undef'), default='undef')
    m_0607 = Column(Enum('true','false','undef'), default='undef')
    m_0608 = Column(Float, default=0.0)
    m_0609 = Column(Float, default=0.0)
    m_0610 = Column(Float, default=0.0)
    m_0611 = Column(Enum('true','false','undef'), default='undef')
    m_0612 = Column(String(8), default='')
    m_0613 = Column(Enum('true','false','undef'), default='undef')
    m_0614 = Column(Enum('true','false','undef'), default='undef')
    m_0615 = Column(Float, default=0.0)
    m_0616 = Column(Float, default=0.0)
    m_0617 = Column(Float, default=0.0)
    m_0618 = Column(Enum('true','false','undef'), default='undef')
    m_0619 = Column(Enum('true','false','undef'), default='undef')
    m_0620 = Column(Integer, default=0)
    m_0621 = Column(Integer, default=0)
    m_0622 = Column(Enum('true','false','undef'), default='undef')
    m_0623 = Column(Integer, default=0)
    m_0624 = Column(Integer, default=0)
    m_0700 = Column(Time, default=datetime.time())
    m_0701 = Column(Date, default=datetime.date.min)
    m_0702 = Column(String(8), default='')
    m_0703 = Column(String(8), default='')
    m_0704 = Column(String(8), default='')
    m_0705 = Column(String(8), default='')
    m_0706 = Column(String(8), default='')
    m_0707 = Column(Float, default=0.0)
    m_0708 = Column(Float, default=0.0)
    m_0709 = Column(Float, default=0.0)
    m_0710 = Column(Float, default=0.0)
    m_0711 = Column(Float, default=0.0)
    m_0712 = Column(Float, default=0.0)
    m_0713 = Column(Float, default=0.0)
    m_0714 = Column(Float, default=0.0)
    m_0715 = Column(String(8), default='')
    m_0716 = Column(String(8), default='')
    m_0717 = Column(Float, default=0.0)
    m_0718 = Column(Enum('true','false','undef'), default='undef')
    m_0800 = Column(String(8), default='')
    m_0801 = Column(String(8), default='')
    m_0802 = Column(String(8), default='')
    m_0803 = Column(String(8), default='')
    m_0804 = Column(String(8), default='')
    m_0805 = Column(String(8), default='')
    m_0806 = Column(String(8), default='')
    m_0807 = Column(Integer, default=0)
    m_0808 = Column(String(8), default='')
    m_0809 = Column(String(8), default='')
    m_0810 = Column(String(8), default='')
    m_0811 = Column(String(8), default='')
    m_0812 = Column(String(8), default='')
    m_0900 = Column(String(8), default='')
    DO_buffer = Column('m_0901', String(8), default='')
    DI_buffer = Column('m_0902', String(8), default='')
    m_0903 = Column(Integer, default=0)
    m_0904 = Column(Integer, default=0)
    m_0905 = Column(Integer, default=0)
    m_0906 = Column(Integer, default=0)
    m_0910 = Column(String(8), default='')
    m_0911 = Column(String(8), default='')
    m_0912 = Column(String(8), default='')
    m_1000 = Column(Integer, default=0)
    m_1001 = Column(Enum('true','false','undef'), default='undef')
    m_1002 = Column(Enum('true','false','undef'), default='undef')
    m_1003 = Column(Time, default=datetime.time())
    m_1004 = Column(Date, default=datetime.date.min)
    m_1005 = Column(Integer, default=0)
    m_1006 = Column(Integer, default=0)
    m_1007 = Column(Integer, default=0)
    m_1008 = Column(Integer, default=0)
    m_1009 = Column(Integer, default=0)

    def __init__(self, columns_and_values):
        if not 'tsp' in columns_and_values:
            self.tsp = time.mktime(datetime.datetime.now().timetuple())
        for columns in columns_and_values:
            setattr(self, columns, columns_and_values[columns])

    @classmethod
    def get_latest(cls, session, columns):
        cc = ColumnCalculator(columns)
        menu_entries = cls.map_names_to_attributes(columns)
        menu_entries = cc.add_entries(menu_entries)

        query = session.query(*menu_entries)
        query = query.order_by(cls.id.desc())
        entry = query.first()

        return cc.calculate_entries(entry)

    @classmethod
    def map_names_to_attributes(cls, names):
        return map(lambda n: getattr(cls, n, None), names)

    @classmethod
    def get_values_in_timespan(cls, session, columns,
                               start, end, quantity=30):
        cc = ColumnCalculator(columns)
        menu_entries = cls.map_names_to_attributes(columns)
        menu_entries = cc.add_entries(menu_entries)

        avg_columns = map(func.avg, menu_entries)

        ret = []
        
        for avg_start, avg_end in _avg_timespan_iter(start, end, quantity):
            query = session.query(*avg_columns)
            query = query.filter(cls.tsp.between(avg_start,
                                                 avg_end))
            result = query.all()[0]
            
            if result[0] is not None:
                ret.append(cc.calculate_entries(result))
        return ret

def _avg_timespan_iter(start, end, quantity):
    start_tsp = int(time.mktime(start.timetuple()))
    end_tsp = int(time.mktime(end.timetuple()))
    delta_start_end = end_tsp - start_tsp
    step = delta_start_end/quantity

    for avg_start in range(start_tsp, end_tsp, step):
        yield (avg_start, avg_start + step)

