from db import db
from sqlalchemy import Column, Index, Text, Integer, Numeric, CHAR


class Ticker(db.Model):

    __tablename__ = "ticker"
    __table_args__ = (
        Index('timestamp_idx', 'timestamp', unique=False),
    )

    id = Column(Integer, primary_key=True)

    pair = Column(CHAR(7))

    a_price = Column(Numeric(18, 5))
    a_whole_lot_volume = Column(Numeric(18, 8))
    a_lot_volume = Column(Numeric(18, 8))

    b_price = Column(Numeric(18, 5))
    b_whole_lot_volume = Column(Numeric(18, 8))
    b_lot_volume = Column(Numeric(18, 8))

    c_price = Column(Numeric(18, 5))
    c_lot_volume = Column(Numeric(18, 8))

    v_today = Column(Numeric(18, 8))
    v_24_hours = Column(Numeric(18, 8))

    p_today = Column(Numeric(18, 5))
    p_24_hours = Column(Numeric(18, 5))

    t_today = Column(Integer)
    t_24_hours = Column(Integer)

    l_today = Column(Numeric(18, 5))
    l_24_hours = Column(Numeric(18, 5))

    h_today = Column(Numeric(18, 5))
    h_24_hours = Column(Numeric(18, 5))

    o_today = Column(Numeric(18, 5))
    o_24_hours = Column(Numeric(18, 5))

    timestamp = Column(Numeric(18, 5))


class Trades(db.Model):

    __tablename__ = "trades"
    __table_args__ = (
        Index('idx_time', "time"),
    )

    id = Column(Integer(), primary_key=True)
    pair = Column(Text())
    price = Column(Numeric(18,5))
    volume = Column(Numeric(18,5))
    time = Column(Numeric(18,5))
    side = Column(Text())
    order_type = Column(Text())
    misc = Column(Text())



class ActiveAPI(db.Model):

    __tablename__ = "active_api"

    api_name = Column(Text(), primary_key=True)
    api_key = Column(Text())