from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import insert

Base = declarative_base()
engine = create_engine("postgresql+pg8000://son:nos@localhost/jobDB")

class JobDB(Base):
    __tablename__ = 'job'
    job_id = Column(String(50),primary_key=True)
    job_title = Column(Text,nullable=False)
    company_id = Column(String(50),nullable=False)
    company_name = Column(Text,nullable=False)
    company_size = Column(Text,nullable=True)
    location = Column(Text)
    job_function = Column(Text)
    group_job_function = Column(String(500))
    created_on = Column(Text)
    salary_max = Column(Text)
    salary_min = Column(Text)
    salary_estimate = Column(Text)
    job_level = Column(Text)
    application = Column(Text)
    view = Column(Text)
    job_board = Column(String(10))

try:
  Base.metadata.create_all(engine)
except:
  Base.metadata.drop_all(engine)
  Base.metadata.create_all(engine)

def insert_data(values):
  
  Session = sessionmaker(bind=engine)
  session = Session()

  insert_stmt = insert(JobDB).values(values)
  on_conflict_update_stmt = insert_stmt.on_conflict_do_update(index_elements=['job_id'],
  set_={'created_on': insert_stmt.excluded.created_on})
  try:
    session.execute(on_conflict_update_stmt)
    session.commit()
  except Exception as e:
    session.rollback()
    print(f"Error: {e}")