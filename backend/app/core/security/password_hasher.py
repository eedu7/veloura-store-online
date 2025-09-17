import bcrypt


class PasswordHasher:
    @staticmethod
    def hash(password: str, rounds: int = 12) -> str:
        if not password:
            raise ValueError("Password cannot be empty or null")

        hashed = bcrypt.hashpw(password.encode("utf*8"), bcrypt.gensalt(rounds))
        return hashed.decode("utf-8")

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        if not plain_password or not hashed_password:
            raise ValueError("Passwrods cannot be empty or null")

        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf*8"))
