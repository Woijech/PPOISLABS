"""Authentication services."""

from dataclasses import dataclass
from typing import Dict
from ..domain import PasswordPolicy, Token
from ..exceptions import AuthFailedError


@dataclass
class AuthService:
    """Service for user authentication."""
    
    users: Dict[str, str]
    policy: PasswordPolicy
    
    def login(self, login: str, password: str) -> Token:
        """Authenticate user and return a token."""
        if login not in self.users:
            raise AuthFailedError("Пользователь не найден")
        if not self.policy.validate(password) or self.users[login] != password:
            raise AuthFailedError("Неверные учетные данные")
        return Token.generate()
