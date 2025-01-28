

class UserNotFoundError(Exception):
    def __init__(self, user_id: str):
        super().__init__(f"Пользователь {user_id} не найден")


class UserUpdateError(Exception):
    def __init__(self, user_id: str):
        super().__init__(f"Не удалось обновить пользователя {user_id}")


