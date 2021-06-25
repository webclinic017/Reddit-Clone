import bcrypt


def hash(string: str) -> str:
    """Helper function to hash a string and return the hash as a string"""
    return bcrypt.hashpw(string.encode(), bcrypt.gensalt()).decode()


def checkPasswordMatchesHash(password: str, hash: str) -> bool:
    """Helper function to check if a string matched a given hash"""
    return bcrypt.checkpw(password.encode(), hash.encode())
