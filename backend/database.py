from sqlmodel import SQLModel, create_engine, Session

# UPDATE THIS WITH YOUR POSTGRES CREDENTIALS
POSTGRES_URL = "postgresql://user:password@localhost:5432/mercyanna_db"

engine = create_engine(POSTGRES_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session