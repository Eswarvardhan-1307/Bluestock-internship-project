from sqlalchemy import create_engine, text

# Create/connect to SQLite database
engine = create_engine("sqlite:///sql/bluestock_mf.db")

# Read schema.sql
with open("sql/schema.sql", "r") as file:
    schema = file.read()

# Execute each SQL statement
with engine.begin() as conn:
    for statement in schema.split(";"):
        statement = statement.strip()
        if statement:
            conn.execute(text(statement))

print("Database and tables created successfully!") 

