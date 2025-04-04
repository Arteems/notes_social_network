from fastapi import HTTPException, status


class UserNotFoundError(HTTPException):
    def __init__(self, user_data):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            detail=f"Поиск пользователя {user_data} не дал результатов",
        )


class UserUpdateError(HTTPException):
    def __init__(self, user_id: str):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Не удалось обновить пользователя {user_id}",
        )


class InvalidUserRoleError(HTTPException):
    def __init__(self, user_id: str):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            detail=f"Не подходящая роль пользователя {user_id}",
        )


class UsernameAlreadyExistsError(HTTPException):
    def __init__(self, username: str):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Username {username} уже занят",
        )


class EmailAlreadyExistsError(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Почта {email} уже занята",
        )
