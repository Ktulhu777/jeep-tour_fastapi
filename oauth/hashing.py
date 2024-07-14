from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        """Метод проверяет на соответствие паролей
        plain_password - пароль от пользователя;
        hashed_password - пароль из БД"""
        return password_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Выдает зашешированный пароль"""
        return password_context.hash(password)

