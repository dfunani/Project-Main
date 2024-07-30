from sqlalchemy import create_engine, Column, String, Integer, DateTime, Date, Time, JSON, Boolean
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import declarative_base, Session
import datetime

import config

Base = declarative_base()

engine = create_engine(
    f"{config.sql}://{config.user}:{config.password}@{config.host}:{config.port}/{config.dbName}")


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    dev_profile = Column(ENUM("Python", "C", "Full-Stack",
                              "Unity", "Android", name="myUsers2"))

    def Read(self, statement):
        with Session(engine) as session:
            result = session.execute(statement)
        return {'id': self.id, 'action': 'read', 'status': result}

    def Serializer(self):
        return {'id': self.id, 'name': self.name, 'dev_profile': self.dev_profile}


class Processes(Base):

    __tablename__ = "Processes"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    batch_location = Column(String(255), nullable=False)
    project_location = Column(String(255), nullable=False)
    next_runtime = Column(DateTime(), nullable=False,
                          default=datetime.datetime.now())
    last_runtime = Column(DateTime(), nullable=False,
                          default=datetime.datetime.now())
    exec_duration = Column(Time(), nullable=True)
    outcome = Column(String(50), nullable=True)
    log_location = Column(String(255), nullable=True)
    exec_by = Column(Integer, ForeignKey("User.id"), nullable=True)
    triggers = Column(ENUM("Hourly", "Daily", "Weekly",
                           "Monthly", "Quarter", "Bi-Annually", "Yearly", "Email", name="triggerENUM"), nullable=False)
    args = Column(JSON(), nullable=True)
    enabled = Column(Boolean(), default=False)
    createdby = Column(Integer, ForeignKey("User.id"), nullable=True)
    createdate = Column(DateTime(), nullable=False,
                        default=datetime.datetime.now())

    def Read(self, statement):
        # statement = select(User).filter_by(name="ed") (.all() is added to the return value)
        with Session(engine) as session:
            result = session.execute(statement).all()
        return {'id': 0, 'action': 'read', 'status': result}

    def Create(self):
        try:
            with Session(engine) as session:
                session.add(self)
                result = self
        except:
            result = "Error"
        return {'id': self.id, 'action': 'create', 'result': result}

    def Update(self, statement):
        # statement: Update(object).where(model.field == value).values(updateField = newValue).execution_options(synchronize_session="fetch")
        with Session(engine) as session:
            session.execute(statement)
            result = self
        return {'id': self.id, 'action': 'update', 'result': result}

    def Delete(self):
        with Session(engine) as session:
            session.delete(self)
            result = self
        return {'id': self.id, 'action': 'delete', 'result': result}

    def Serializer(self):
        return {
            "id": self.id,
            "name": self.name,
            "batch_location": self.batch_location,
            "project_location": self.project_location,
            "next_runtime": self.next_runtime,
            "last_runtime": self.last_runtime,
            "exec_duration ": self.exec_duration,
            "outcome": self.outcome,
            "log_location": self.log_location,
            "exec_by": self.exec_by,
            "triggers": self.triggers,
            "enabled": self.enabled,
            "createdby": self.createdby,
            "createdate": self.createdate
        }


class Email(Base):
    __tablename__ = "Email"

    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey("Processes.id"))
    subject = Column(String, nullable=False)

    def Read(self, statement):
        with Session(engine) as session:
            result = session.execute(statement)
        return {'id': self.id, 'action': 'create', 'status': result}

    def Serializer(self):
        return {'id': self.id, 'process_id': self.process_id, 'subject': self.subject}


def Get(model, id):
    with Session(engine) as session:
        result = session.get(model, id)
    return {'id': id, 'action': 'get', 'status': result}


def Create_All(models):
    try:
        with Session(engine) as session:
            session.add_all(models)
            result = models
    except:
        result = "Error"
    return {'id': 0, 'action': 'create_all', 'result': result}
