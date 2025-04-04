from fastapi import HTTPException, status


class UserNotFoundError(HTTPException):
    def __init__(self, user_id: str):
        super().__init__(
            status.HTTP_404_NOT_FOUND, detail=f"Пользователь {user_id} не найден"
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
