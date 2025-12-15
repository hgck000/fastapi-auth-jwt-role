import sys
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.user import User

def main(email: str):
    db = SessionLocal()
    try:
        user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
        if not user:
            print("User not found:", email)
            sys.exit(1)
        user.role = "admin"
        db.commit()
        print("Updated role to admin for:", email)
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.scripts.make_admin <email>")
        sys.exit(1)
    main(sys.argv[1])
