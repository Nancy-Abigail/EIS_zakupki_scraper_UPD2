from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, String, FLOAT
from sqlalchemy.orm import relationship, sessionmaker, Session, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from lov import oktmo_to_city_name

engine = create_engine('sqlite:///database/result.sqlite', echo=False, connect_args={'check_same_thread': False})
Base = declarative_base()


# It's easier to control session at an orchestrator side to control its lifecycle and avoid using same session
# in different threads. All commits, rollbacks and session closures should be managed at an orchestrator side as well.
def new_session() -> Session:
    return scoped_session(sessionmaker(bind=engine))


# Technical tables (association tables, etc.)
x_contract_contractors = Table(
    'x_contract_contractors',
    Base.metadata,
    Column('contract_number', Integer, ForeignKey('t_contracts.registry_number')),
    Column('contractor_inn', Integer, ForeignKey('t_contractors.inn'))
)


# Basic tables
class Contract(Base):
    # Table
    __tablename__ = 't_contracts'

    # Columns
    registry_number = Column(Integer, primary_key=True)
    client_inn = Column(Integer, ForeignKey('t_clients.inn'))
    contract_date = Column(String)
    execution_date = Column(String)
    contract_price = Column(FLOAT)

    # Relationships
    client = relationship('Client', back_populates='contracts')
    contractors = relationship('Contractor', secondary=x_contract_contractors, back_populates='contracts')
    items = relationship('Item', back_populates='contract')

    def push(self, session: Session):
        """
        Adds an item to database or updates if it already exists.

        :param session: sqlalchemy.orm.Session
        :return: orm.Contract - self if it's a new item, or updated origin.
        If you want to work with this object - rewrite it with output of this function.
        """
        # Check if item already exists
        origin = session.query(self.__class__).\
            filter(self.__class__.registry_number == self.registry_number).\
            first()

        # If yes - update
        if origin is not None:
            origin.contract_date = self.contract_date
            origin.execution_date = self.execution_date
            origin.contract_price = self.contract_price
            return origin
        # If not - add to database
        else:
            session.add(self)
            return self

    def clear_items(self, session: Session):
        for item in self.items:
            session.delete(item)


class Client(Base):
    # Table
    __tablename__ = 't_clients'

    # Columns
    inn = Column(Integer, primary_key=True)
    name = Column(String)
    city_oktmo = Column(Integer, ForeignKey('t_cities.oktmo'))

    # Relationships
    contracts = relationship('Contract', back_populates='client')
    city = relationship('City', back_populates='clients')

    def push(self, session: Session):
        """
        Adds an item to database or updates if it already exists.

        :param session: sqlalchemy.orm.Session
        :return: orm.Client - self if it's a new item, or updated origin.
        If you want to work with this object - rewrite it with output of this function.
        """
        # Check if item already exists
        origin = session.query(self.__class__).\
            filter(self.__class__.inn == self.inn).\
            first()

        # If yes - update
        if origin is not None:
            origin.name = self.name
            origin.city_oktmo = self.city_oktmo
            return origin
        # If not - add to database
        else:
            session.add(self)
            return self


class City(Base):
    # Table
    __tablename__ = 't_cities'

    # Columns
    oktmo = Column(Integer, primary_key=True)
    name = Column(String)

    # Relationships
    clients = relationship('Client', back_populates='city')

    @classmethod
    def add_city(cls, oktmo, name, session: Session):
        origin = session.query(cls).\
            filter(cls.oktmo == oktmo).\
            first()

        if origin is None:
            city = cls(oktmo=oktmo, name=name)
            session.add(city)


class Contractor(Base):
    # Table
    __tablename__ = 't_contractors'

    # Columns
    inn = Column(Integer, primary_key=True)
    name = Column(String)
    full_address = Column(String)

    # Relationships
    contracts = relationship('Contract', secondary=x_contract_contractors, back_populates='contractors')

    def push(self, session: Session):
        """
        Adds an item to database or updates if it already exists.

        :param session: sqlalchemy.orm.Session
        :return: orm.Contractor - self if it's a new item, or updated origin.
        If you want to work with this object - rewrite it with output of this function.
        """
        # Check if item already exists
        origin = session.query(self.__class__).\
            filter(self.__class__.inn == self.inn).\
            first()

        # If yes - update
        if origin is not None:
            origin.name = self.name
            origin.full_address = self.full_address
            return origin
        # If not - add to database
        else:
            session.add(self)
            return self


class Item(Base):
    # Table
    __tablename__ = 't_items'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_number = Column(Integer, ForeignKey('t_contracts.registry_number'))
    okpd_code = Column(Integer)
    name = Column(String)
    price = Column(FLOAT)

    # Relationships
    contract = relationship('Contract', back_populates='items')

    def push(self, session: Session):
        """
        Adds an item to database.

        :param session: sqlalchemy.orm.Session
        :return: self
        """

        session.add(self)
        return self


def initialize_database():
    # Create database schema
    Base.metadata.create_all(engine)

    # Fill cities table
    session = new_session()
    for key, value in oktmo_to_city_name.items():
        City.add_city(int(key), value, session)
    session.commit()
    session.close()


if __name__ == '__main__':
    initialize_database()
