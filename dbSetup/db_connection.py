import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = sqlalchemy.create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    fullname = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return ("User(name='{s.name}', fullname='{s.fullname}', "
                "password='{s.password}')").format(s=self)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
    session = Session()
    session.add(ed_user)
    session.commit()
    our_user = session.query(User).filter_by(name='ed').all()
    print(our_user)
