import subprocess
import sys

def run_migrations():
    try:
        print("Starting Migrations")
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Migrations completed")
    except subprocess.CalledProcessError as e:
        print("Migrations error", e)
        sys.exit(1)

def start_app():
    print("Starting API")
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    run_migrations()
    start_app()