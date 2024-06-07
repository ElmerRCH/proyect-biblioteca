from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate(email: str, password: str, collection):
    user = collection.find_one({"email": email})
    if not user:
        return False

    if not verify_password(password, user['password']):
        return False
    return user
    