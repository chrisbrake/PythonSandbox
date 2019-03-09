import contextlib
import logging
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

Base = declarative_base()
engine = sqlalchemy.create_engine('sqlite:///', echo=False)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    fullname = sqlalchemy.Column(sqlalchemy.String, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String, server_default='passwd')

    def __repr__(self):
        return ("User(id='{s.id}', name='{s.name}', fullname='{s.fullname}', "
                "password='{s.password}')").format(s=self)

    def __str__(self):
        return json.dumps({
            k: v for (k, v) in self.__dict__.items() if not k.startswith('_')
        })


Base.metadata.create_all(engine)


@contextlib.contextmanager
def session():
    s = Session()
    yield s
    s.commit()
    s.close()


def diag(req, resp):
    logging.debug('tables %s', engine.table_names())
    logging.debug('driver %s', engine.driver)
    return {'driver': engine.driver}
