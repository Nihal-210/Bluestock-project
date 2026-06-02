import sys
print(sys.executable)
from sqlalchemy import create_engine, text

engine = create_engine(
    "sqlite:///bluestock_mf.db"
)

with open("sql/schema.sql", "r") as f:
    schema = f.read()

with engine.connect() as conn:

    for statement in schema.split(";"):

        if statement.strip():

            conn.execute(
                text(statement)
            )

    conn.commit()

print("Database and tables created successfully.")