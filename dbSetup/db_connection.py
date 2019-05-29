import json
import logging
from contextlib import contextmanager

from sqlalchemy import create_engine, String, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

logging.basicConfig(level=logging.DEBUG)
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
        # Write ed
        ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
        # s.add(ed_user)  # This will throw an IntegrityError second run
        s.merge(ed_user)  # This will not

    with session() as s:
        # Read back ed
        ed = s.query(User).filter_by(name='ed').one()
        logger.info('ed: %s', ed)

    with session() as s:
        # Write an order placed by ed
        ed_order = Order(user_id=ed.id)
        s.merge(ed_order)
        logger.info('ed_order: %s', ed_order)

    with session() as s:
        # Read back ed's order
        order = s.query(Order).join(User).filter_by(name='ed').all()
        logger.info('order: %s', order)

    with session() as s:
        # Write some more orders placed by ed
        ed_order = Order(user_id=ed.id)
        s.bulk_save_objects([Order(user_id=ed.id) for _ in range(2)])
        logger.info('ed_order: %s', ed_order)

    with session() as s:
        # Read back ed's orders
        orders = s.query(Order).join(User).filter_by(name='ed').all()
        logger.info('orders: %s', orders)

    with session() as s:
        # Build out francine's history
        s.merge(User(
            name='frankie', fullname='Francine Fournier', password='password'))
        frankie = s.query(User).filter_by(name='frankie').one()
        s.bulk_save_objects([Order(user_id=frankie.id) for _ in range(2)])

    with session() as s:
        # Read back francine's orders
        logger.info("All orders: %s", s.query(Order).all())
        logger.info("Frankie's orders: %s",
                    s.query(Order).join(User).filter_by(name='frankie').all())

    with session() as s:
        for i, o in enumerate(s.query(Order).all()):
            logger.info(
                "%d result: %s placed order %d", i, o.user.name, o.id)

        for u in s.query(User).all():
            logger.info(
                "%s placed orders %s", u.name,
                ', '.join([str(o.id) for o in u.orders]))
