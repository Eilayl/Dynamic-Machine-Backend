from sqlmodel import SQLModel, create_engine, Session

engine = create_engine('sqlite:///streampay.db', echo=True)  
SQLModel.metadata.create_all(engine)

# 
def get_session():
    with Session(engine) as session:
        yield session