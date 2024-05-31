from dataclasses import dataclass


@dataclass
class BotUser:
    """
        Базовый класс юзера телеграм бота
            tg_user_id: int, - идентификатор юзера из телеграмма
            tg_first_name: str | None,
            tg_last_name: str | None,
            is_registred: bool = False,
            is_admin: bool = False,
        """
    def __init__(self,
                 bot_user_id: int | None,
                 is_admin: bool | None,
                 loodsman_id: int | None,
                 first_name: str | None,
                 last_name: str | None,
                 is_registred: bool = False,
                 ):
        self.bot_user_id = bot_user_id
        self.is_admin = is_admin
        self.loodsman_id = loodsman_id
        self.first_name = first_name
        self.last_name = last_name
        self.is_registred = is_registred

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
