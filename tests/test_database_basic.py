import os
import sys
import unittest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from database import (  # type: ignore  # noqa: E402
    init_database,
    seed_data,
    authenticate_user,
    get_completed_requests_count,
    get_average_repair_time,
)


class DatabaseBasicTests(unittest.TestCase):
    """Базовые тесты работы с БД для демонстрационного экзамена."""

    @classmethod
    def setUpClass(cls) -> None:
        init_database()
        seed_data()

    def test_authenticate_valid_user(self) -> None:
        """Авторизация с корректными учетными данными должна проходить успешно."""
        user = authenticate_user("login1", "pass1")
        self.assertIsNotNone(user)

    def test_completed_requests_count_non_negative(self) -> None:
        """Количество выполненных заявок не должно быть отрицательным."""
        count = get_completed_requests_count()
        self.assertGreaterEqual(count, 0)

    def test_average_repair_time_not_negative(self) -> None:
        """Среднее время ремонта не должно быть отрицательным."""
        avg = get_average_repair_time()
        self.assertGreaterEqual(avg, 0.0)


if __name__ == "__main__":
    unittest.main()

