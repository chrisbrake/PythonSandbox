import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

Base = declarative_base()
engine = sqlalchemy.create_engine('sqlite:///test.db', echo=True)
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


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
    session = Session()
    # session.add(ed_user)  # This will throw an IntegrityError second run
    session.merge(ed_user)  # This will not
    try:
        session.commit()
    except IntegrityError as ie:
        print('Error:', ie)
        session.rollback()

    our_users = session.query(User).filter_by(name='ed').all()
    print('All users: {}'.format(our_users))
    print('Filter example {i.id}: {i.fullname}'.format(
        i=session.query(User).filter_by(id=1).one()))
