from db_init import SessionLocal, engine
from sqlalchemy import text

# Method 2: Using raw SQL
session = SessionLocal()
try:
    result = session.execute(text("SELECT * FROM staging_course LIMIT 10"))
    for row in result:
        print(row)
finally:
    session.close()