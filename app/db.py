from sqlmodel import create_engine, SQLModel


sqlite_url = "sqlite:///./habits.db"
engine = create_engine(sqlite_url, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)