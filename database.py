import sqlite3
from typing import List

from config import DB_PATH
from models import User, Request


def init_database() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT NOT NULL,
            phone TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            type TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Requests (
            requestID INTEGER PRIMARY KEY AUTOINCREMENT,
            startDate TEXT NOT NULL,
            carType TEXT NOT NULL,
            carModel TEXT NOT NULL,
            problemDescryption TEXT NOT NULL,
            requestStatus TEXT DEFAULT 'Новая заявка',
            completionDate TEXT,
            repairParts TEXT,
            masterID INTEGER,
            clientID INTEGER NOT NULL,
            FOREIGN KEY (masterID) REFERENCES Users(userID),
            FOREIGN KEY (clientID) REFERENCES Users(userID)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Comments (
            commentID INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            masterID INTEGER NOT NULL,
            requestID INTEGER NOT NULL,
            createdDate TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (masterID) REFERENCES Users(userID),
            FOREIGN KEY (requestID) REFERENCES Requests(requestID) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


def seed_data() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    users_data = [
        (1, "Белов Александр Давидович", "89210563128", "login1", "pass1", "Менеджер"),
        (2, "Харитонова Мария Павловна", "89535078985", "login2", "pass2", "Автомеханик"),
        (3, "Марков Давид Иванович", "89210673849", "login3", "pass3", "Автомеханик"),
        (4, "Громова Анна Семёновна", "89990563748", "login4", "pass4", "Оператор"),
        (5, "Карташова Мария Данииловна", "89994563847", "login5", "pass5", "Оператор"),
        (6, "Касаткин Егор Львович", "89219567849", "login11", "pass11", "Заказчик"),
        (7, "Ильина Тамара Даниловна", "89219567841", "login12", "pass12", "Заказчик"),
        (8, "Елисеева Юлиана Алексеевна", "89219567842", "login13", "pass13", "Заказчик"),
        (9, "Никифорова Алиса Тимофеевна", "89219567843", "login14", "pass14", "Заказчик"),
        (10, "Васильев Али Евгеньевич", "89219567844", "login15", "pass15", "Автомеханик"),
        (11, "Петрова Мария Ивановна", "89123456789", "login16", "pass16", "Менеджер по качеству"),
        (12, "Козлов Сергей Николаевич", "89161234567", "mgr2", "mgr2", "Менеджер"),
        (13, "Соколова Ольга Викторовна", "89167654321", "op6", "op6", "Оператор"),
        (14, "Волков Дмитрий Андреевич", "89165551234", "op7", "op7", "Оператор"),
        (15, "Новикова Елена Игоревна", "89167778899", "op8", "op8", "Оператор"),
        (16, "Федоров Иван Петрович", "89163334455", "mech4", "mech4", "Автомеханик"),
        (17, "Морозова Светлана Александровна", "89169990011", "mech5", "mech5", "Автомеханик"),
        (18, "Кузнецов Андрей Сергеевич", "89162223344", "mech6", "mech6", "Автомеханик"),
        (19, "Смирнов Павел Олегович", "89161112233", "client5", "client5", "Заказчик"),
        (20, "Попова Наталья Дмитриевна", "89164445566", "client6", "client6", "Заказчик"),
        (21, "Семёнов Роман Владимирович", "89167779988", "client7", "client7", "Заказчик"),
        (22, "Михайлова Кристина Андреевна", "89168880099", "client8", "client8", "Заказчик"),
        (23, "Лебедев Артём Ильич", "89160001122", "client9", "client9", "Заказчик"),
        (24, "Козлова Виктория Павловна", "89163336699", "client10", "client10", "Заказчик"),
        (25, "Орлов Максим Станиславович", "89165557788", "q2", "q2", "Менеджер по качеству"),
    ]
    requests_data = [
        (1, "2023-06-06", "Легковая", "Hyundai Avante (CN7)", "Отказали тормоза.", "В процессе ремонта", None, "", 2, 7),
        (2, "2023-05-05", "Легковая", "Nissan 180SX ", "Отказали тормоза.", "В процессе ремонта", None, "", 3, 8),
        (3, "2022-07-07", "Легковая", "Toyota 2000GT ", "В салоне пахнет бензином.", "Готова к выдаче", "2023-01-01", "", 3, 9),
        (4, "2023-08-02", "Грузовая", "Citroen Berlingo (B9)", "Руль плохо крутится.", "Новая заявка", None, "", None, 8),
        (5, "2023-08-02", "Грузовая", "УАЗ 2360 ", "Руль плохо крутится.", "Новая заявка", None, "", None, 9),
        (6, "2024-01-10", "Легковая", "Lada Vesta", "Стук в подвеске.", "В процессе ремонта", None, "", 2, 6),
        (7, "2024-01-12", "Легковая", "Kia Rio", "Замена масла, ТО.", "В процессе ремонта", None, "", 2, 7),
        (8, "2024-01-14", "Грузовая", "ГАЗель Next", "Развал-схождение.", "Новая заявка", None, "", 3, 8),
        (9, "2024-01-15", "Легковая", "Volkswagen Polo", "Проверка кондиционера.", "В процессе ремонта", None, "", 3, 9),
        (10, "2024-01-16", "Легковая", "Skoda Octavia", "Замена тормозных колодок.", "В процессе ремонта", None, "", 10, 6),
        (11, "2024-01-18", "Внедорожник", "Toyota RAV4", "Диагностика двигателя.", "В процессе ремонта", None, "", 10, 7),
        (12, "2024-01-20", "Легковая", "Hyundai Solaris", "Прокол колеса, ремонт.", "Новая заявка", None, "", 2, 8),
        (13, "2024-01-22", "Грузовая", "Mercedes Sprinter", "Замена ремня ГРМ.", "В процессе ремонта", None, "", 3, 9),
        (14, "2024-01-25", "Легковая", "Mazda 3", "Не заводится с утра.", "В процессе ремонта", None, "", 10, 6),
        (15, "2024-01-26", "Легковая", "Ford Focus", "Треск при повороте руля.", "Новая заявка", None, "", 2, 8),
    ]
    comments_data = [
        (1, "Очень странно.", 2, 1),
        (2, "Будем разбираться!", 3, 2),
        (3, "Будем разбираться!", 3, 3),
    ]
    try:
        cur.executemany(
            "INSERT OR IGNORE INTO Users (userID, fio, phone, login, password, type) VALUES (?, ?, ?, ?, ?, ?)",
            users_data,
        )
        cur.executemany(
            "INSERT OR IGNORE INTO Requests (requestID, startDate, carType, carModel, problemDescryption, requestStatus, completionDate, repairParts, masterID, clientID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            requests_data,
        )
        cur.executemany(
            "INSERT OR IGNORE INTO Comments (commentID, message, masterID, requestID) VALUES (?, ?, ?, ?)",
            comments_data,
        )
        conn.commit()
    except Exception as exc:
        print(f"[ERROR] Ошибка загрузки данных: {exc}")
    finally:
        conn.close()


def authenticate_user(login: str, password: str) -> User | None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT userID, fio, phone, login, password, type FROM Users WHERE login = ? AND password = ?",
            (login, password),
        )
        row = cur.fetchone()
        if row:
            return User(user_id=row[0], fio=row[1], phone=row[2], login=row[3], password=row[4], user_type=row[5])
        return None
    except Exception as exc:
        print(f"[ERROR] Ошибка авторизации: {exc}")
        return None
    finally:
        conn.close()


def get_completed_requests_count() -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute('SELECT COUNT(*) FROM Requests WHERE requestStatus = "Готова к выдаче"')
        return int(cur.fetchone()[0])
    except Exception as exc:
        print(f"[ERROR] Ошибка подсчёта заявок: {exc}")
        return 0
    finally:
        conn.close()


def get_average_repair_time() -> float:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT julianday(completionDate) - julianday(startDate)
            FROM Requests
            WHERE requestStatus = 'Готова к выдаче' AND completionDate IS NOT NULL
        """)
        rows = cur.fetchall()
        if not rows:
            return 0.0
        return round(sum(r[0] for r in rows) / len(rows), 2)
    except Exception as exc:
        print(f"[ERROR] Ошибка расчёта среднего времени: {exc}")
        return 0.0
    finally:
        conn.close()


def get_all_requests() -> List[Request]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT r.requestID, r.startDate, r.carType, r.carModel, r.problemDescryption,
                   r.requestStatus, r.completionDate, r.repairParts, r.masterID, r.clientID,
                   m.fio, c.fio
            FROM Requests r
            LEFT JOIN Users m ON r.masterID = m.userID
            LEFT JOIN Users c ON r.clientID = c.userID
        """)
        out: List[Request] = []
        for row in cur.fetchall():
            req = Request(
                request_id=row[0],
                start_date=row[1],
                car_type=row[2],
                car_model=row[3],
                problem_descryption=row[4],
                request_status=row[5],
                completion_date=row[6],
                repair_parts=row[7],
                master_id=row[8],
                client_id=row[9],
                master_name=row[10] or "Не назначен",
                client_name=row[11] or "",
            )
            out.append(req)
        return out
    except Exception as exc:
        print(f"[ERROR] Ошибка загрузки заявок: {exc}")
        return []
    finally:
        conn.close()


def get_comments_for_request(request_id: int) -> list:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT c.message, u.fio, c.createdDate
            FROM Comments c
            JOIN Users u ON c.masterID = u.userID
            WHERE c.requestID = ?
        """, (request_id,))
        return cur.fetchall()
    except Exception as exc:
        print(f"[ERROR] Ошибка загрузки комментариев: {exc}")
        return []
    finally:
        conn.close()


def get_users_by_type(user_type: str) -> List[tuple]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("SELECT userID, fio FROM Users WHERE type = ? ORDER BY fio", (user_type,))
        return cur.fetchall()
    except Exception as exc:
        print(f"[ERROR] Ошибка загрузки пользователей: {exc}")
        return []
    finally:
        conn.close()


def create_request(
    start_date: str,
    car_type: str,
    car_model: str,
    problem_descryption: str,
    client_id: int,
    master_id: int | None = None,
) -> int | None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Requests (startDate, carType, carModel, problemDescryption, requestStatus, repairParts, masterID, clientID)
            VALUES (?, ?, ?, ?, 'Новая заявка', '', ?, ?)
        """, (start_date, car_type.strip(), car_model.strip(), problem_descryption.strip(), master_id, client_id))
        conn.commit()
        return cur.lastrowid
    except Exception as exc:
        print(f"[ERROR] Ошибка создания заявки: {exc}")
        return None
    finally:
        conn.close()


def get_request_by_id(request_id: int) -> tuple | None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT r.startDate, r.carType, r.carModel, r.problemDescryption, r.requestStatus,
                   r.completionDate, r.repairParts, m.fio, c.fio
            FROM Requests r
            LEFT JOIN Users m ON r.masterID = m.userID
            LEFT JOIN Users c ON r.clientID = c.userID
            WHERE r.requestID = ?
        """, (request_id,))
        return cur.fetchone()
    except Exception as exc:
        print(f"[ERROR] Ошибка загрузки заявки: {exc}")
        return None
    finally:
        conn.close()


def get_request_status_and_master(request_id: int) -> tuple | None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("SELECT requestStatus, masterID FROM Requests WHERE requestID = ?", (request_id,))
        return cur.fetchone()
    except Exception as exc:
        print(f"[ERROR] Ошибка загрузки заявки: {exc}")
        return None
    finally:
        conn.close()


def update_request_status(request_id: int, new_status: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        from datetime import date
        completion_date = date.today().isoformat() if new_status == "Готова к выдаче" else None
        if completion_date:
            cur.execute(
                "UPDATE Requests SET requestStatus = ?, completionDate = ? WHERE requestID = ?",
                (new_status, completion_date, request_id),
            )
        else:
            cur.execute(
                "UPDATE Requests SET requestStatus = ?, completionDate = NULL WHERE requestID = ?",
                (new_status, request_id),
            )
        conn.commit()
        return cur.rowcount > 0
    except Exception as exc:
        print(f"[ERROR] Ошибка обновления статуса: {exc}")
        return False
    finally:
        conn.close()


def update_request_master(request_id: int, master_id: int | None) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("UPDATE Requests SET masterID = ? WHERE requestID = ?", (master_id, request_id))
        conn.commit()
        return cur.rowcount > 0
    except Exception as exc:
        print(f"[ERROR] Ошибка назначения механика: {exc}")
        return False
    finally:
        conn.close()


def add_comment(request_id: int, master_id: int, message: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Comments (message, masterID, requestID) VALUES (?, ?, ?)",
            (message.strip(), master_id, request_id),
        )
        conn.commit()
        return True
    except Exception as exc:
        print(f"[ERROR] Ошибка добавления комментария: {exc}")
        return False
    finally:
        conn.close()


def delete_request(request_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Comments WHERE requestID = ?", (request_id,))
        cur.execute("DELETE FROM Requests WHERE requestID = ?", (request_id,))
        conn.commit()
        return True
    except Exception as exc:
        print(f"[ERROR] Ошибка удаления заявки: {exc}")
        return False
    finally:
        conn.close()
