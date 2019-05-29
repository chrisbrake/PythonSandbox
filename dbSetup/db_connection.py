import json
import logging
from contextlib import contextmanager

from sqlalchemy import create_engine, String, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

engine = create_engine('sqlite:///', echo=False)
Session = sessionmaker(bind=engine)


@contextmanager
def session():
    s = Session()
    try:
        yield s
        s.commit()
    except IntegrityError as ie:
        logger.exception('Unhandled %s exception.', ie)
        s.rollback()


@as_declarative()
class Base(object):
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    def dumps(self):
        return json.dumps({
            k: v for (k, v) in self.__dict__.items() if not k.startswith('_')
        })

    def __str__(self):
        return self.dumps()

    def __repr__(self):
        return self.dumps()


class User(Base):
    name = Column(String, nullable=False)
    fullname = Column(String, unique=True)
    password = Column(String, server_default='passwd')
    orders = relationship('Order', back_populates='user')


class Order(Base):
    user = relationship('User', back_populates='orders')
    user_id = Column(Integer, ForeignKey('user.id'))


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    with session() as s:
        # write ed
        ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
        # s.add(ed_user)  # This will throw an IntegrityError second run
        s.merge(ed_user)  # This will not

    with session() as s:
        # Read back ed
        ed = s.query(User).filter_by(name='ed').one()
        print('ed: ', ed)

    with session() as s:
        # write an order placed by ed
        ed_order = Order(user_id=ed.id)
        s.merge(ed_order)
        print('ed_order: ', ed_order)

    with session() as s:
        # Read back ed's order
        order = s.query(Order).join(User).filter_by(name='ed').all()
        print('order', order)
