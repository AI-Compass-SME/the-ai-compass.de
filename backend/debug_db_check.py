from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

# Force load env from backend directory
load_dotenv()

db_url = os.getenv("DATABASE_URL")
print(f"Connecting to: {db_url.split('@')[1] if '@' in db_url else 'LOCAL/SQLITE'}")

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        print("--- Row Counts ---")
        for table in ["companies", "responses", "questions", "dimensions"]:
            try:
                result = conn.execute(text(f"SELECT count(*) FROM {table}"))
                count = result.scalar()
                print(f"{table}: {count}")
            except Exception as e:
                print(f"{table}: Error {e}")
except Exception as e:
    print(f"Connection Failed: {e}")
