from db_init import SessionLocal, engine
from sqlalchemy import text, inspect

# Method 2: Using raw SQL
session = SessionLocal()
try:
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    for table in tables:
        print(table)
        result = session.execute(text(f"SELECT * FROM {table} LIMIT 1"))
        for row in result:
            print(row)
        print('~~~~')
finally:
    session.close()


