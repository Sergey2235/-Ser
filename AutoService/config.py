

# Путь к базе данных
DB_PATH = "AutoService.db"

# Цветовая палитра (Material Design)
BG_COLOR = "#f0f4f8"
CARD_BG = "#ffffff"
HEADER_BG = "#1e3a5f"
HEADER_FG = "#ffffff"
BTN_COLOR = "#2563eb"
BTN_HOVER = "#1d4ed8"
TEXT_COLOR = "#1e293b"
TEXT_MUTED = "#64748b"
ACCENT = "#0ea5e9"
SUCCESS = "#22c55e"
DANGER = "#ef4444"
WARNING = "#f59e0b"

# Шрифты и размеры
FONT_FAMILY = "Segoe UI"
FONT_SIZE = 10
FONT_HEADER = 14
FONT_TITLE = 20
PAD = 12
RADIUS = 8

# Ссылка на опрос качества (Модуль 3)
QUALITY_SURVEY_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdhZcExx6LSIXxk0ub55mSu-WIh23WYdGG9HY5EZhLDo7P8eA/viewform?usp=sf_link"

# Статусы заявок
REQUEST_STATUSES = ("Новая заявка", "В процессе ремонта", "Готова к выдаче")

# Цвета статусов для визуального выделения в списке заявок
STATUS_COLORS = {
    "Новая заявка": "#e0f2fe",          # светло-синий
    "В процессе ремонта": "#fef9c3",    # светло-жёлтый
    "Готова к выдаче": "#dcfce7",       # светло-зелёный
}

# Типы автомобилей
CAR_TYPES = ("Легковая", "Грузовая", "Внедорожник")

# Роли пользователей
USER_ROLES = ("Менеджер", "Менеджер по качеству", "Оператор", "Автомеханик", "Заказчик")