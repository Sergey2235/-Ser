from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    user_id: Optional[int] = None
    fio: str = ""
    phone: str = ""
    login: str = ""
    password: str = ""
    user_type: str = ""


@dataclass
class Request:
    request_id: Optional[int] = None
    start_date: str = ""
    car_type: str = ""
    car_model: str = ""
    problem_descryption: str = ""
    request_status: str = "Новая заявка"
    completion_date: Optional[str] = None
    repair_parts: Optional[str] = None
    master_id: Optional[int] = None
    client_id: Optional[int] = None
    master_name: str = "Не назначен"
    client_name: str = ""

    def __post_init__(self):
        if not self.start_date:
            self.start_date = datetime.now().strftime("%Y-%m-%d")


@dataclass
class Comment:
    comment_id: Optional[int] = None
    message: str = ""
    master_id: Optional[int] = None
    request_id: Optional[int] = None
    created_date: str = ""

    def __post_init__(self):
        if not self.created_date:
            self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
