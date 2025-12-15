from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.core.security import get_password_hash, verify_password

def main():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

    pw = "123456"
    hpw = get_password_hash(pw)
    print("Sample hash:", hpw)
    print("Verify:", verify_password(pw, hpw))

if __name__ == "__main__":
    main()
