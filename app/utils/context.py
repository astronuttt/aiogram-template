from contextvars import ContextVar

from app.models.user import User

current_user: ContextVar[User] = ContextVar("current_user", default=None)
