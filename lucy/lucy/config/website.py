from dataclasses import dataclass
from typing import Optional

from lucy.types import Token


@dataclass
class WebsiteConfig:
    host: str
    user_id: Optional[str] = None
    passwd: Optional[str] = None
    token: Optional[Token] = None
    auth_token_name: str = 'REVEL_SESSION'
    login_path: str = 'login'
    protected_path: str = 'settings'

    @property
    def login_url(self) -> str:
        return f'{self.host}/{self.login_path}'

    @property
    def protected_url(self) -> str:
        return f'{self.host}/{self.protected_path}'

    @property
    def cookie(self) -> dict[str, str]:
        assert self.token
        return {'name': self.auth_token_name, 'value': self.token.value}
