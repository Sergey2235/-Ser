

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional, Callable
from config import (
    BG_COLOR,
    CARD_BG,
    HEADER_BG,
    HEADER_FG,
    BTN_COLOR,
    BTN_HOVER,
    TEXT_MUTED,
    SUCCESS,
    DANGER,
    PAD,
    FONT_FAMILY,
    FONT_HEADER,
    FONT_TITLE,
    QUALITY_SURVEY_URL,
    REQUEST_STATUSES,
    CAR_TYPES,
    STATUS_COLORS,
)
from database import (
    authenticate_user,
    get_all_requests,
    get_request_by_id,
    get_request_status_and_master,
    get_users_by_type,
    create_request,
    update_request_status,
    update_request_master,
    add_comment,
    delete_request,
    get_comments_for_request,
    get_completed_requests_count,
    get_average_repair_time,
    backup_database,
    create_user,
    update_request_details,
)
from models import User

# Проверка доступности библиотек для QR-кода
try:
    import qrcode
    from PIL import ImageTk, Image
    QR_CODE_AVAILABLE = True
except ImportError:
    QR_CODE_AVAILABLE = False


def _setup_styles() -> None:
    """Настройка стилей виджетов"""
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
    style.configure("Treeview", rowheight=28, font=(FONT_FAMILY, 10))
    style.configure("Treeview.Heading", font=(FONT_FAMILY, 10, "bold"))
    style.configure("TCombobox", padding=6)


def _apply_button_hover(button: tk.Button, normal_bg: str, hover_bg: Optional[str] = None) -> None:
    """Простое наведение для кнопок"""
    if hover_bg is None:
        hover_bg = BTN_HOVER

    def on_enter(_event: tk.Event) -> None:
        button.configure(bg=hover_bg)

    def on_leave(_event: tk.Event) -> None:
        button.configure(bg=normal_bg)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)


def _add_placeholder(entry: tk.Entry, placeholder: str) -> None:
    """Плейсхолдер для Entry (очищается при фокусе)"""
    if entry.get().strip():
        return

    entry.insert(0, placeholder)
    entry.configure(fg=TEXT_MUTED)

    def on_focus_in(_event: tk.Event) -> None:
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(fg="black")

    def on_focus_out(_event: tk.Event) -> None:
        if not entry.get().strip():
            entry.insert(0, placeholder)
            entry.configure(fg=TEXT_MUTED)

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


class LoginForm:
    """Форма авторизации пользователя"""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Авторизация — АвтоТранс")
        self.root.geometry("420x380")
        self.root.resizable(False, False)
        self.root.config(bg=BG_COLOR)
        _setup_styles()
        self._build_ui()
        self._center_window()

    def _build_ui(self) -> None:
        card = tk.Frame(self.root, bg=CARD_BG, padx=PAD * 2, pady=PAD * 2)
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(card, text="🚗 АвтоТранс", font=(FONT_FAMILY, FONT_TITLE, "bold"), 
                 fg=HEADER_BG, bg=CARD_BG).pack(pady=(0, PAD * 2))
        tk.Label(card, text="Вход в систему", font=(FONT_FAMILY, 11), 
                 fg=TEXT_MUTED, bg=CARD_BG).pack(pady=(0, PAD))
        
        tk.Label(card, text="Логин:", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w")
        self.entry_login = tk.Entry(card, width=32, font=(FONT_FAMILY, 11), 
                                    relief="solid", bd=1)
        self.entry_login.pack(pady=(2, PAD))
        
        tk.Label(card, text="Пароль:", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w")
        self.entry_password = tk.Entry(card, show="*", width=32, 
                                       font=(FONT_FAMILY, 11), relief="solid", bd=1)
        self.entry_password.pack(pady=(2, PAD))
        
        login_btn = tk.Button(
            card,
            text="Войти",
            bg=BTN_COLOR,
            fg="white",
            font=(FONT_FAMILY, 10),
            relief="flat",
            padx=24,
            pady=8,
            cursor="hand2",
            command=self._login,
        )
        login_btn.pack(pady=PAD)
        _apply_button_hover(login_btn, BTN_COLOR)

        reg_btn = tk.Button(
            card,
            text="Регистрация",
            bg="white",
            fg=BTN_COLOR,
            font=(FONT_FAMILY, 9),
            relief="solid",
            bd=1,
            padx=20,
            pady=6,
            cursor="hand2",
            command=self._open_register,
        )
        reg_btn.pack(pady=(0, PAD))
        
        hint = tk.Frame(self.root, bg=BG_COLOR)
        hint.place(relx=0.5, rely=0.92, anchor="center")
        tk.Label(hint, text="Менеджер: login1/pass1 · Оператор: login4/pass4 · Механик: login2/pass2", 
                 font=(FONT_FAMILY, 8), fg=TEXT_MUTED, bg=BG_COLOR).pack()

    def _center_window(self) -> None:
        self.root.update_idletasks()
        w, h = 420, 380
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _login(self) -> None:
        login = self.entry_login.get().strip()
        password = self.entry_password.get().strip()
        
        if not login or not password:
            messagebox.showwarning("Ошибка ввода", "Введите логин и пароль.")
            return
        
        user = authenticate_user(login, password)
        if user:
            messagebox.showinfo("Успех", f"Добро пожаловать, {user.fio} ({user.user_type})!")
            self.root.destroy()
            new_root = tk.Tk()
            MainForm(new_root, user)
            new_root.mainloop()
        else:
            messagebox.showerror("Ошибка входа", "Неверный логин или пароль.")

    def _open_register(self) -> None:
        win = tk.Toplevel(self.root)
        RegisterForm(win)


class RegisterForm:
    """Окно регистрации нового пользователя (заказчика)"""

    def __init__(self, root: tk.Toplevel) -> None:
        self.root = root
        self.root.title("Регистрация пользователя")
        self.root.geometry("460x420")
        self.root.resizable(False, False)
        self.root.config(bg=BG_COLOR)
        _setup_styles()
        self._build_ui()
        self._center_window()

    def _build_ui(self) -> None:
        card = tk.Frame(self.root, bg=CARD_BG, padx=PAD * 2, pady=PAD * 2)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card,
            text="Регистрация",
            font=(FONT_FAMILY, FONT_HEADER, "bold"),
            fg=HEADER_BG,
            bg=CARD_BG,
        ).pack(pady=(0, PAD * 2))

        tk.Label(card, text="ФИО:", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w")
        self.entry_fio = tk.Entry(card, width=36, font=(FONT_FAMILY, 10), relief="solid", bd=1)
        self.entry_fio.pack(pady=(2, PAD))
        _add_placeholder(self.entry_fio, "Иванов Иван Иванович")

        tk.Label(card, text="Телефон:", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w")
        self.entry_phone = tk.Entry(card, width=36, font=(FONT_FAMILY, 10), relief="solid", bd=1)
        self.entry_phone.pack(pady=(2, PAD))
        _add_placeholder(self.entry_phone, "89991234567")

        tk.Label(card, text="Логин:", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w")
        self.entry_login = tk.Entry(card, width=36, font=(FONT_FAMILY, 10), relief="solid", bd=1)
        self.entry_login.pack(pady=(2, PAD))
        _add_placeholder(self.entry_login, "login_new")

        tk.Label(card, text="Пароль:", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w")
        self.entry_password = tk.Entry(card, show="*", width=36, font=(FONT_FAMILY, 10), relief="solid", bd=1)
        self.entry_password.pack(pady=(2, PAD))

        tk.Label(card, text="Подтверждение пароля:", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w")
        self.entry_password2 = tk.Entry(card, show="*", width=36, font=(FONT_FAMILY, 10), relief="solid", bd=1)
        self.entry_password2.pack(pady=(2, PAD))

        hint = tk.Label(
            card,
            text="Новый пользователь будет зарегистрирован как заказчик.",
            font=(FONT_FAMILY, 8),
            fg=TEXT_MUTED,
            bg=CARD_BG,
            wraplength=360,
            justify="left",
        )
        hint.pack(pady=(0, PAD))

        btn_frame = tk.Frame(card, bg=CARD_BG)
        btn_frame.pack(pady=(PAD // 2, 0))

        save_btn = tk.Button(
            btn_frame,
            text="Зарегистрироваться",
            bg=SUCCESS,
            fg="white",
            font=(FONT_FAMILY, 10),
            relief="flat",
            padx=18,
            pady=6,
            cursor="hand2",
            command=self._save,
        )
        save_btn.pack(side="left", padx=6)
        _apply_button_hover(save_btn, SUCCESS, "#16a34a")

        cancel_btn = tk.Button(
            btn_frame,
            text="Отмена",
            bg="white",
            fg=TEXT_MUTED,
            font=(FONT_FAMILY, 10),
            relief="solid",
            bd=1,
            padx=18,
            pady=6,
            cursor="hand2",
            command=self.root.destroy,
        )
        cancel_btn.pack(side="left", padx=6)

    def _center_window(self) -> None:
        self.root.update_idletasks()
        w, h = 460, 420
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _save(self) -> None:
        fio = self.entry_fio.get().strip()
        phone = self.entry_phone.get().strip()
        login = self.entry_login.get().strip()
        pwd1 = self.entry_password.get().strip()
        pwd2 = self.entry_password2.get().strip()

        # Убрать плейсхолдеры, если пользователь их не заменил
        if fio == "Иванов Иван Иванович":
            fio = ""
        if phone == "89991234567":
            phone = ""
        if login == "login_new":
            login = ""

        if not fio or not phone or not login or not pwd1 or not pwd2:
            messagebox.showwarning("Ошибка ввода", "Заполните все поля.")
            return
        if pwd1 != pwd2:
            messagebox.showwarning("Ошибка ввода", "Пароли не совпадают.")
            return

        new_id = create_user(fio=fio, phone=phone, login=login, password=pwd1, user_type="Заказчик")
        if new_id is None:
            messagebox.showerror(
                "Ошибка регистрации",
                "Не удалось создать пользователя.\nВозможно, логин уже занят. Попробуйте другой логин.",
            )
            return

        messagebox.showinfo(
            "Успех",
            "Пользователь успешно зарегистрирован.\nТеперь вы можете войти, используя указанные логин и пароль.",
        )
        self.root.destroy()


class MainForm:
    """Главное меню приложения"""
    
    def __init__(self, root: tk.Tk, user: User) -> None:
        self.root = root
        self.user = user
        self.root.title(f"АвтоТранс — личный кабинет ({user.user_type})")
        self.root.geometry("860x620")
        self.root.resizable(True, True)
        self.root.config(bg=BG_COLOR)
        
        self._build_header()
        self._build_content()

    def _build_header(self) -> None:
        header = tk.Frame(self.root, bg=HEADER_BG, height=56)
        header.pack(fill="x")
        tk.Label(header, text=f"🚗 АвтоТранс · {self.user.fio}", 
                 fg=HEADER_FG, bg=HEADER_BG, font=(FONT_FAMILY, 12)).pack(side="left", padx=PAD * 2, pady=14)
        logout_btn = tk.Button(
            header,
            text="Выход",
            bg=DANGER,
            fg="white",
            font=(FONT_FAMILY, 10),
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            command=self._logout,
        )
        logout_btn.pack(side="right", padx=PAD * 2, pady=10)
        _apply_button_hover(logout_btn, DANGER, "#dc2626")

    def _build_content(self) -> None:
        content = tk.Frame(self.root, bg=BG_COLOR, padx=PAD * 3, pady=PAD * 3)
        content.pack(fill="both", expand=True)
        
        # "Hero"-карточка с приветствием и ролью
        hero_outer = tk.Frame(content, bg=BG_COLOR)
        hero_outer.pack(fill="x", pady=(0, PAD * 2))
        hero = tk.Frame(hero_outer, bg=CARD_BG, padx=PAD * 2, pady=PAD * 2)
        hero.pack(fill="x")
        
        tk.Label(
            hero,
            text=f"Добро пожаловать, {self.user.fio}!",
            font=(FONT_FAMILY, 18, "bold"),
            bg=CARD_BG,
        ).pack(anchor="w")
        tk.Label(
            hero,
            text=f"Роль в системе: {self.user.user_type}",
            font=(FONT_FAMILY, 11),
            fg=TEXT_MUTED,
            bg=CARD_BG,
        ).pack(anchor="w", pady=(4, 0))
        
        # Основная зона: слева меню, справа краткая сводка
        body = tk.Frame(content, bg=BG_COLOR)
        body.pack(fill="both", expand=True)
        
        # Левая колонка — меню действий
        menu_card = tk.Frame(body, bg=CARD_BG, padx=PAD * 2, pady=PAD * 2)
        menu_card.pack(side="left", fill="y", padx=(0, PAD * 2))
        
        tk.Label(
            menu_card,
            text="Навигация",
            font=(FONT_FAMILY, 12, "bold"),
            bg=CARD_BG,
        ).pack(anchor="w", pady=(0, PAD))
        
        if self.user.user_type in ("Оператор", "Менеджер", "Менеджер по качеству"):
            btn_requests = tk.Button(
                menu_card,
                text="📋 Заявки",
                bg=BTN_COLOR,
                fg="white",
                font=(FONT_FAMILY, 11),
                relief="flat",
                padx=20,
                pady=10,
                cursor="hand2",
                command=self._open_requests,
            )
            btn_requests.pack(fill="x", pady=4)
            _apply_button_hover(btn_requests, BTN_COLOR)
        
            btn_stats = tk.Button(
                menu_card,
                text="📊 Статистика",
                bg=BTN_COLOR,
                fg="white",
                font=(FONT_FAMILY, 11),
                relief="flat",
                padx=20,
                pady=10,
                cursor="hand2",
                command=self._open_statistics,
            )
            btn_stats.pack(fill="x", pady=4)
            _apply_button_hover(btn_stats, BTN_COLOR)
        
            # Резервное копирование (Модуль 2)
            btn_backup = tk.Button(
                menu_card,
                text="💾 Резервная копия БД",
                bg=SUCCESS,
                fg="white",
                font=(FONT_FAMILY, 11),
                relief="flat",
                padx=20,
                pady=10,
                cursor="hand2",
                command=self._backup_db,
            )
            btn_backup.pack(fill="x", pady=(8, 0))
            _apply_button_hover(btn_backup, SUCCESS, "#16a34a")
        elif self.user.user_type in ("Автомеханик", "Заказчик"):
            btn_my_reqs = tk.Button(
                menu_card,
                text="📋 Мои заявки",
                bg=BTN_COLOR,
                fg="white",
                font=(FONT_FAMILY, 11),
                relief="flat",
                padx=20,
                pady=10,
                cursor="hand2",
                command=self._open_requests,
            )
            btn_my_reqs.pack(fill="x", pady=4)
            _apply_button_hover(btn_my_reqs, BTN_COLOR)
        
        # Правая колонка — краткая статистика по заявкам (для служебных ролей)
        summary_card = tk.Frame(body, bg=CARD_BG, padx=PAD * 2, pady=PAD * 2)
        summary_card.pack(side="left", fill="both", expand=True)
        
        tk.Label(
            summary_card,
            text="Краткая сводка",
            font=(FONT_FAMILY, 12, "bold"),
            bg=CARD_BG,
        ).pack(anchor="w", pady=(0, PAD))
        
        if self.user.user_type in ("Оператор", "Менеджер", "Менеджер по качеству"):
            all_reqs = get_all_requests()
            total_r = len(all_reqs)
            active_r = sum(1 for r in all_reqs if r.request_status != "Готова к выдаче")
            completed_r = sum(1 for r in all_reqs if r.request_status == "Готова к выдаче")
            
            tk.Label(
                summary_card,
                text=f"Всего заявок: {total_r}",
                font=(FONT_FAMILY, 11),
                bg=CARD_BG,
            ).pack(anchor="w", pady=2)
            tk.Label(
                summary_card,
                text=f"Активные в работе: {active_r}",
                font=(FONT_FAMILY, 11),
                bg=CARD_BG,
            ).pack(anchor="w", pady=2)
            tk.Label(
                summary_card,
                text=f"Готовы к выдаче: {completed_r}",
                font=(FONT_FAMILY, 11),
                bg=CARD_BG,
            ).pack(anchor="w", pady=2)
        else:
            tk.Label(
                summary_card,
                text="Здесь будут отображаться основные показатели по вашим заявкам.",
                font=(FONT_FAMILY, 10),
                fg=TEXT_MUTED,
                bg=CARD_BG,
                wraplength=360,
                justify="left",
            ).pack(anchor="w", pady=2)
        
        # Информирование о роли Менеджер по качеству (Модуль 3)
        if self.user.user_type == "Менеджер по качеству":
            messagebox.showinfo(
                "Информация",
                "Вы вошли как Менеджер по качеству.\n"
                "Вы можете контролировать качество, анализировать статистику и взаимодействовать с механиками.",
            )

    def _open_requests(self) -> None:
        RequestsForm(tk.Toplevel(self.root), self.user)

    def _open_statistics(self) -> None:
        StatisticsForm(tk.Toplevel(self.root))

    def _backup_db(self) -> None:
        path = backup_database()
        if path:
            messagebox.showinfo("Успех", f"Резервная копия создана:\n{path}")
        else:
            messagebox.showerror("Ошибка", "Не удалось создать резервную копию.")

    def _logout(self) -> None:
        self.root.destroy()
        new_root = tk.Tk()
        LoginForm(new_root)
        new_root.mainloop()


class RequestsForm:
    """Форма списка заявок"""
    
    def __init__(self, root: tk.Toplevel, user: User) -> None:
        self.root = root
        self.user = user
        self.root.title("Список заявок")
        self.root.geometry("1140x680")
        self.root.config(bg=BG_COLOR)
        
        self._build_header()
        self._build_filters()
        self._build_tree()
        self._load_requests()

    def _build_header(self) -> None:
        header = tk.Frame(self.root, bg=HEADER_BG, height=48)
        header.pack(fill="x")
        tk.Label(header, text="📋 Заявки", fg=HEADER_FG, 
                 bg=HEADER_BG, font=(FONT_FAMILY, 12)).pack(side="left", padx=PAD * 2, pady=12)
        
        add_btn = tk.Button(
            header,
            text="➕ Добавить заявку",
            bg=SUCCESS,
            fg="white",
            font=(FONT_FAMILY, 10),
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self._open_new_request,
        )
        add_btn.pack(side="right", padx=6, pady=10)
        _apply_button_hover(add_btn, SUCCESS, "#16a34a")
        
        back_btn = tk.Button(
            header,
            text="Назад",
            fg=HEADER_FG,
            bg=HEADER_BG,
            font=(FONT_FAMILY, 10),
            relief="flat",
            cursor="hand2",
            command=self.root.destroy,
        )
        back_btn.pack(side="right", padx=PAD, pady=10)
        _apply_button_hover(back_btn, HEADER_BG, "#0f172a")

    def _build_filters(self) -> None:
        filter_frame = tk.Frame(self.root, bg=CARD_BG, padx=PAD, pady=PAD)
        filter_frame.pack(fill="x", padx=PAD, pady=PAD)
        
        tk.Label(filter_frame, text="Статус:", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(side="left")
        self.combo_status = ttk.Combobox(filter_frame, values=("Все",) + REQUEST_STATUSES, 
                                         width=18, state="readonly")
        self.combo_status.set("Все")
        self.combo_status.pack(side="left", padx=4)
        self.combo_status.bind("<<ComboboxSelected>>", lambda e: self._load_requests())
        
        tk.Label(filter_frame, text="Поиск:", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(side="left", padx=(PAD, 0))
        self.entry_search = tk.Entry(filter_frame, width=28, font=(FONT_FAMILY, 10), relief="solid", bd=1)
        self.entry_search.pack(side="left", padx=6, pady=4)
        
        tk.Button(filter_frame, text="Найти", bg=BTN_COLOR, fg="white", 
                  font=(FONT_FAMILY, 10), relief="flat", padx=12, pady=4, 
                  cursor="hand2", command=self._load_requests).pack(side="left", padx=2)
        tk.Button(filter_frame, text="Сбросить", font=(FONT_FAMILY, 10), 
                  relief="flat", cursor="hand2", command=self._reset_search).pack(side="left", padx=2)
        
        self.summary_label = tk.Label(filter_frame, text="", bg=CARD_BG, fg=TEXT_MUTED, font=(FONT_FAMILY, 10))
        self.summary_label.pack(side="right")

    def _build_tree(self) -> None:
        tree_frame = tk.Frame(self.root, bg=BG_COLOR)
        tree_frame.pack(fill="both", expand=True, padx=PAD, pady=(0, PAD))
        
        columns = ("ID", "Дата", "Тип", "Модель", "Проблема", "Статус", "Клиент", "Механик")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=18)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип")
        self.tree.heading("Модель", text="Модель")
        self.tree.heading("Проблема", text="Проблема")
        self.tree.heading("Статус", text="Статус")
        self.tree.heading("Клиент", text="Клиент")
        self.tree.heading("Механик", text="Механик")

        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Дата", width=100, anchor="center")
        self.tree.column("Тип", width=100, anchor="center")
        self.tree.column("Модель", width=160, anchor="w")
        self.tree.column("Проблема", width=260, anchor="w")
        self.tree.column("Статус", width=140, anchor="center")
        self.tree.column("Клиент", width=160, anchor="w")
        self.tree.column("Механик", width=160, anchor="w")
        
        # Цветовые теги по статусу заявки
        self.tree.tag_configure("status_new", background=STATUS_COLORS.get("Новая заявка", ""))
        self.tree.tag_configure("status_in_progress", background=STATUS_COLORS.get("В процессе ремонта", ""))
        self.tree.tag_configure("status_done", background=STATUS_COLORS.get("Готова к выдаче", ""))

        self.tree.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill=tk.Y)
        self.tree.bind("<Double-1>", self._on_double_click)

    def _load_requests(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        status_filter = self.combo_status.get().strip() if hasattr(self, "combo_status") else "Все"
        if status_filter == "":
            status_filter = "Все"
        
        search_text = self.entry_search.get().strip() or None
        requests = get_all_requests()
        
        total = 0
        visible = 0
        
        for req in requests:
            total += 1
            
            # Фильтрация по роли
            if self.user.user_type == "Заказчик" and req.client_id != self.user.user_id:
                continue
            if self.user.user_type == "Автомеханик" and req.master_id != self.user.user_id:
                continue
            if status_filter != "Все" and req.request_status != status_filter:
                continue
            if search_text:
                q = search_text.lower()
                haystack = f"{req.car_model} {req.problem_descryption} {req.client_name}".lower()
                if q not in haystack:
                    continue
            
            visible += 1

            if req.request_status == "Новая заявка":
                tag = "status_new"
            elif req.request_status == "В процессе ремонта":
                tag = "status_in_progress"
            elif req.request_status == "Готова к выдаче":
                tag = "status_done"
            else:
                tag = ""

            self.tree.insert(
                "",
                tk.END,
                values=(
                    req.request_id,
                    req.start_date,
                    req.car_type,
                    req.car_model,
                    req.problem_descryption,
                    req.request_status,
                    req.client_name,
                    req.master_name,
                ),
                tags=(tag,),
            )
        
        self.summary_label.config(text=f"Показано: {visible} из {total}")
        
        if (search_text or status_filter != "Все") and visible == 0:
            messagebox.showinfo("Информация", "По заданным критериям заявки не найдены.")

    def _reset_search(self) -> None:
        self.entry_search.delete(0, tk.END)
        if hasattr(self, "combo_status"):
            self.combo_status.set("Все")
        self._load_requests()

    def _open_new_request(self) -> None:
        NewRequestForm(tk.Toplevel(self.root), self.user, self._load_requests)

    def _on_double_click(self, event) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        if vals:
            RequestDetailsForm(tk.Toplevel(self.root), self.user, int(vals[0]), on_close=self._load_requests)


class NewRequestForm:
    """Форма создания новой заявки"""
    
    def __init__(self, root: tk.Toplevel, current_user: User, on_success: Callable) -> None:
        self.root = root
        self.current_user = current_user
        self.on_success = on_success
        self.root.title("Новая заявка")
        self.root.geometry("500x460")
        self.root.config(bg=BG_COLOR)
        self.root.transient(self.root.master)
        self.root.grab_set()
        
        self._build_form()

    def _build_form(self) -> None:
        clients = get_users_by_type("Заказчик")
        mechanics = get_users_by_type("Автомеханик")
        
        card = tk.Frame(self.root, bg=CARD_BG, padx=PAD * 2, pady=PAD * 2)
        card.pack(fill="both", expand=True, padx=PAD, pady=PAD)
        
        # Клиент
        tk.Label(card, text="Клиент (заказчик):", font=(FONT_FAMILY, 10), bg=CARD_BG).grid(row=0, column=0, sticky="w", pady=6)
        self.client_ids = [row[0] for row in clients]
        self.client_names = [row[1] for row in clients]

        # Если текущий пользователь сам является заказчиком,
        # показываем в списке только его, чтобы он создавал заявки от своего имени.
        if self.current_user.user_type == "Заказчик":
            for cid, cname in zip(self.client_ids, self.client_names):
                if cid == self.current_user.user_id:
                    self.client_ids = [cid]
                    self.client_names = [cname]
                    break
        self.combo_client = ttk.Combobox(card, values=self.client_names, width=40, state="readonly")
        self.combo_client.grid(row=0, column=1, pady=6, padx=PAD)
        if self.client_names:
            self.combo_client.current(0)
        
        # Тип авто
        tk.Label(card, text="Тип авто:", font=(FONT_FAMILY, 10), bg=CARD_BG).grid(row=1, column=0, sticky="w", pady=6)
        self.combo_car_type = ttk.Combobox(card, values=CAR_TYPES, width=38, state="readonly")
        self.combo_car_type.grid(row=1, column=1, pady=6, padx=PAD)
        self.combo_car_type.set(CAR_TYPES[0])
        
        # Модель
        tk.Label(card, text="Модель авто:", font=(FONT_FAMILY, 10), bg=CARD_BG).grid(row=2, column=0, sticky="w", pady=6)
        self.entry_model = tk.Entry(card, width=42, font=(FONT_FAMILY, 10), relief="solid", bd=1)
        self.entry_model.grid(row=2, column=1, pady=6, padx=PAD)
        
        # Проблема
        tk.Label(card, text="Описание проблемы:", font=(FONT_FAMILY, 10), bg=CARD_BG).grid(row=3, column=0, sticky="nw", pady=6)
        self.entry_problem = tk.Text(card, width=40, height=4, wrap="word", font=(FONT_FAMILY, 10), relief="solid", bd=1)
        self.entry_problem.grid(row=3, column=1, pady=6, padx=PAD)
        
        # Механик
        # Для менеджера/оператора механик выбирается из списка,
        # для заказчика выбор механика при создании заявки не отображается.
        self.master_ids = [None]
        self.master_names = ["— Не назначен"]
        self.combo_master = None
        if self.current_user.user_type in ("Оператор", "Менеджер", "Менеджер по качеству"):
            tk.Label(card, text="Механик (необяз.):", font=(FONT_FAMILY, 10), bg=CARD_BG).grid(
                row=4,
                column=0,
                sticky="w",
                pady=6,
            )
            self.master_ids = [None] + [row[0] for row in mechanics]
            self.master_names = ["— Не назначен"] + [row[1] for row in mechanics]
            self.combo_master = ttk.Combobox(card, values=self.master_names, width=38, state="readonly")
            self.combo_master.grid(row=4, column=1, pady=6, padx=PAD)
            self.combo_master.current(0)
        
        # Кнопки
        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=PAD)
        tk.Button(btn_frame, text="Сохранить", bg=SUCCESS, fg="white", 
                  font=(FONT_FAMILY, 10), relief="flat", padx=20, pady=8, 
                  cursor="hand2", command=self._save).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Отмена", font=(FONT_FAMILY, 10), 
                  relief="flat", cursor="hand2", command=self.root.destroy).pack(side="left", padx=8)

    def _save(self) -> None:
        if not self.client_names:
            messagebox.showwarning("Ошибка", "В системе нет заказчиков.")
            return
        
        idx = self.combo_client.current()
        if idx < 0:
            messagebox.showwarning("Ошибка ввода", "Выберите клиента.")
            return
        
        client_id = self.client_ids[idx]
        car_type = self.combo_car_type.get().strip()
        if not car_type:
            messagebox.showwarning("Ошибка ввода", "Выберите тип авто.")
            return
        
        model = self.entry_model.get().strip()
        if not model:
            messagebox.showwarning("Ошибка ввода", "Введите модель авто.")
            return
        
        problem = self.entry_problem.get("1.0", tk.END).strip()
        if not problem:
            messagebox.showwarning("Ошибка ввода", "Введите описание проблемы.")
            return
        
        master_id = None
        if self.combo_master is not None:
            master_idx = self.combo_master.current()
            master_id = self.master_ids[master_idx] if 0 <= master_idx < len(self.master_ids) else None
        
        from datetime import datetime
        start_date = datetime.now().strftime("%Y-%m-%d")
        
        new_id = create_request(start_date, car_type, model, problem, client_id, master_id)
        if new_id is None:
            messagebox.showerror("Ошибка", "Не удалось создать заявку.")
            return
        
        messagebox.showinfo("Успех", f"Заявка №{new_id} создана.")
        self.on_success()
        self.root.destroy()


class RequestDetailsForm:
    """Форма деталей заявки с комментариями и QR-кодом"""
    
    def __init__(self, root: tk.Toplevel, user: User, request_id: int, on_close: Optional[Callable] = None) -> None:
        self.root = root
        self.user = user
        self.request_id = request_id
        self.on_close = on_close or (lambda: None)
        self.root.title(f"Детали заявки #{request_id}")
        self.root.geometry("840x720")
        self.root.config(bg=BG_COLOR)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self._build_header()
        self._build_content()
        self._build_actions()
        self._build_comments()
        self._build_footer()

    def _build_header(self) -> None:
        header = tk.Frame(self.root, bg=HEADER_BG, height=48)
        header.pack(fill="x")
        tk.Label(header, text=f"📋 Заявка #{self.request_id}", 
                 fg=HEADER_FG, bg=HEADER_BG, font=(FONT_FAMILY, 12)).pack(side="left", padx=PAD * 2, pady=12)
        tk.Button(header, text="Назад", fg=HEADER_FG, bg=HEADER_BG, 
                  font=(FONT_FAMILY, 10), relief="flat", cursor="hand2", 
                  command=self._on_close).pack(side="right", padx=PAD * 2, pady=10)

    def _build_content(self) -> None:
        content = tk.Frame(self.root, bg=BG_COLOR, padx=PAD * 2, pady=PAD)
        content.pack(fill="both", expand=True)
        
        card = tk.Frame(content, bg=CARD_BG, padx=PAD * 2, pady=PAD * 2)
        card.pack(fill="x", pady=(0, PAD))
        
        row = get_request_by_id(self.request_id)
        raw = get_request_status_and_master(self.request_id)
        self.current_status = raw[0] if raw else "Новая заявка"
        self.current_master_id = raw[1] if raw else None
        self.current_client_id = raw[2] if raw else None
        
        if row:
            (
                start_date,
                car_type,
                car_model,
                problem,
                status,
                completion_date,
                repair_parts,
                master_fio,
                client_fio,
            ) = row
            
            tk.Label(card, text=f"Дата приёма: {start_date}", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w", pady=4)
            tk.Label(card, text=f"Тип авто: {car_type}", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w", pady=4)

            # Редактируемая модель авто (по умолчанию заблокирована, включается кнопкой "Редактировать")
            row_model = tk.Frame(card, bg=CARD_BG)
            row_model.pack(fill="x", pady=2)
            tk.Label(row_model, text="Модель:", font=(FONT_FAMILY, 10), bg=CARD_BG, width=16, anchor="w").pack(
                side="left"
            )
            self.entry_car_model = tk.Entry(
                row_model,
                width=60,
                font=(FONT_FAMILY, 10),
                relief="solid",
                bd=1,
            )
            self.entry_car_model.insert(0, car_model)
            self.entry_car_model.pack(side="left", padx=(0, 4))
            self.entry_car_model.configure(state="disabled")

            # Редактируемое описание проблемы
            tk.Label(card, text="Описание проблемы:", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w", pady=(4, 2))
            self.text_problem = tk.Text(
                card,
                width=74,
                height=4,
                wrap="word",
                font=(FONT_FAMILY, 10),
                relief="solid",
                bd=1,
            )
            self.text_problem.insert("1.0", problem)
            self.text_problem.pack(pady=(0, 4))
            self.text_problem.configure(state="disabled")

            tk.Label(card, text=f"Статус: {status}", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w", pady=4)
            tk.Label(card, text=f"Клиент: {client_fio or '—'}", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w", pady=4)
            tk.Label(card, text=f"Механик: {master_fio or 'Не назначен'}", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w", pady=4)
            
            if completion_date:
                tk.Label(card, text=f"Дата завершения: {completion_date}", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w", pady=4)
                try:
                    from datetime import datetime
                    d1 = datetime.strptime(start_date, "%Y-%m-%d")
                    d2 = datetime.strptime(completion_date, "%Y-%m-%d")
                    days = (d2 - d1).days
                    tk.Label(card, text=f"Длительность ремонта: {days} дн.", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w", pady=4)
                except ValueError:
                    pass
            
            tk.Label(card, text="Запчасти (при наличии):", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w", pady=(4, 2))
            self.entry_parts = tk.Entry(
                card,
                width=74,
                font=(FONT_FAMILY, 10),
                relief="solid",
                bd=1,
            )
            if repair_parts and repair_parts.strip():
                self.entry_parts.insert(0, repair_parts.strip())
            self.entry_parts.pack(pady=(0, 4))
            self.entry_parts.configure(state="disabled")

            # Сохранить оригинальные значения (для "Отмена")
            self._orig_car_model = car_model
            self._orig_problem = problem
            self._orig_parts = (repair_parts or "")

    def _build_actions(self) -> None:
        """Панель действий в зависимости от роли"""
        content = tk.Frame(self.root, bg=BG_COLOR, padx=PAD * 2, pady=PAD)
        content.pack(fill="both", expand=True)
        
        can_edit = self.user.user_type in ("Оператор", "Менеджер", "Менеджер по качеству") or (
            self.user.user_type == "Автомеханик" and self.current_master_id == self.user.user_id
        )
        can_edit_client = (
            self.user.user_type == "Заказчик"
            and self.current_client_id == self.user.user_id
            and self.current_status == "Новая заявка"
        )
        can_edit_mech = self.user.user_type in ("Оператор", "Менеджер", "Менеджер по качеству")
        can_comment = can_edit or can_edit_client or (
            self.user.user_type == "Автомеханик" and self.current_master_id == self.user.user_id
        )
        can_delete = self.user.user_type in ("Оператор", "Менеджер")
        
        if can_edit or can_edit_mech or can_comment or can_delete:
            act = tk.Frame(content, bg=CARD_BG, padx=PAD, pady=PAD)
            act.pack(fill="x", pady=(0, PAD))
            tk.Label(act, text="Действия", font=(FONT_FAMILY, 10, "bold"), bg=CARD_BG).pack(anchor="w", pady=(0, 6))
            
            row2 = tk.Frame(act, bg=CARD_BG)
            row2.pack(fill="x")

            # Отдельная кнопка "Редактировать" (включает поля заявки)
            if can_edit or can_edit_client:
                self.btn_edit_details = tk.Button(
                    row2,
                    text="✏️ Редактировать",
                    bg="white",
                    fg=BTN_COLOR,
                    font=(FONT_FAMILY, 9),
                    relief="solid",
                    bd=1,
                    padx=10,
                    pady=4,
                    cursor="hand2",
                    command=self._enable_edit_mode,
                )
                self.btn_edit_details.pack(side="left", padx=(0, 8))
            
            if can_edit or can_edit_client:
                tk.Label(row2, text="Статус:", font=(FONT_FAMILY, 9), bg=CARD_BG).pack(side="left")
                self.combo_status = ttk.Combobox(row2, values=REQUEST_STATUSES, width=20, state="readonly")
                self.combo_status.set(self.current_status)
                self.combo_status.pack(side="left", padx=4)
                tk.Button(row2, text="Сохранить статус", bg=BTN_COLOR, fg="white", 
                          font=(FONT_FAMILY, 9), relief="flat", padx=10, pady=4, 
                          cursor="hand2", command=self._save_status).pack(side="left", padx=8)

                # Кнопка сохранения текстовых полей заявки
                self.btn_save_details = tk.Button(
                    row2,
                    text="Сохранить изменения заявки",
                    bg=SUCCESS,
                    fg="white",
                    font=(FONT_FAMILY, 9),
                    relief="flat",
                    padx=10,
                    pady=4,
                    cursor="hand2",
                    command=self._save_details,
                )
                self.btn_save_details.pack(side="left", padx=8)
                self.btn_save_details.configure(state="disabled")

                self.btn_cancel_details = tk.Button(
                    row2,
                    text="Отмена",
                    bg="white",
                    fg=TEXT_MUTED,
                    font=(FONT_FAMILY, 9),
                    relief="solid",
                    bd=1,
                    padx=10,
                    pady=4,
                    cursor="hand2",
                    command=self._cancel_edit_mode,
                )
                self.btn_cancel_details.pack(side="left", padx=8)
                self.btn_cancel_details.configure(state="disabled")
            
            if can_edit_mech:
                mechanics = get_users_by_type("Автомеханик")
                self.master_ids = [None] + [m[0] for m in mechanics]
                self.master_names = ["— Не назначен"] + [m[1] for m in mechanics]
                tk.Label(row2, text="Механик:", font=(FONT_FAMILY, 9), bg=CARD_BG).pack(side="left", padx=(12, 0))
                self.combo_master = ttk.Combobox(row2, values=self.master_names, width=22, state="readonly")
                idx = self.master_ids.index(self.current_master_id) if self.current_master_id in self.master_ids else 0
                self.combo_master.current(idx)
                self.combo_master.pack(side="left", padx=4)
                tk.Button(row2, text="Назначить", bg=BTN_COLOR, fg="white", 
                          font=(FONT_FAMILY, 9), relief="flat", padx=10, pady=4, 
                          cursor="hand2", command=self._assign_master).pack(side="left", padx=8)
            
            if can_delete:
                tk.Button(row2, text="Удалить заявку", bg=DANGER, fg="white", 
                          font=(FONT_FAMILY, 9), relief="flat", padx=10, pady=4, 
                          cursor="hand2", command=self._delete_request).pack(side="left", padx=8)
        
        if can_comment:
            comm_row = tk.Frame(content, bg=CARD_BG, padx=PAD, pady=PAD)
            comm_row.pack(fill="x", pady=(0, PAD))
            tk.Label(comm_row, text="Новый комментарий:", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w")
            self.entry_comment = tk.Entry(comm_row, width=60, font=(FONT_FAMILY, 10), relief="solid", bd=1)
            self.entry_comment.pack(side="left", padx=(0, 8), pady=4)
            tk.Button(comm_row, text="Добавить", bg=SUCCESS, fg="white", 
                      font=(FONT_FAMILY, 10), relief="flat", padx=12, pady=4, 
                      cursor="hand2", command=self._add_comment).pack(side="left")

    def _build_comments(self) -> None:
        content = tk.Frame(self.root, bg=BG_COLOR, padx=PAD * 2, pady=PAD)
        content.pack(fill="both", expand=True)
        
        tk.Label(content, text="💬 Комментарии", font=(FONT_FAMILY, 11, "bold"), bg=BG_COLOR).pack(anchor="w", pady=(PAD, 4))
        self.comments_card = tk.Frame(content, bg=CARD_BG, padx=PAD, pady=PAD)
        self.comments_card.pack(fill="both", expand=True)
        self._fill_comments()

    def _build_footer(self) -> None:
        """QR-код для опроса качества (Модуль 3)"""
        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=PAD)
        
        if QR_CODE_AVAILABLE:
            tk.Button(btn_frame, text="📱 QR-код для отзыва", bg=SUCCESS, fg="white", 
                      font=(FONT_FAMILY, 10), relief="flat", padx=16, pady=8, 
                      cursor="hand2", command=self._show_qr).pack(side="left", padx=6)
        else:
            tk.Label(btn_frame, text="QR-код недоступен (установите qrcode и Pillow)", 
                     font=(FONT_FAMILY, 9), fg=TEXT_MUTED, bg=BG_COLOR).pack(side="left", padx=6)

    def _fill_comments(self) -> None:
        for w in self.comments_card.winfo_children():
            w.destroy()
        
        comments = get_comments_for_request(self.request_id)
        if comments:
            for msg, author, date in comments:
                tk.Label(self.comments_card, text=f"{author} ({date}): {msg}", 
                         font=(FONT_FAMILY, 9), bg="#e2e8f0", anchor="w").pack(fill="x", padx=6, pady=4)
        else:
            tk.Label(self.comments_card, text="Комментариев нет.", 
                     font=(FONT_FAMILY, 10), fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w", padx=6)

    def _save_status(self) -> None:
        new_status = self.combo_status.get().strip()
        if not new_status or new_status not in REQUEST_STATUSES:
            return
        if update_request_status(self.request_id, new_status):
            self.current_status = new_status
            messagebox.showinfo("Успех", "Статус обновлён.")
        else:
            messagebox.showerror("Ошибка", "Не удалось обновить статус.")

    def _save_details(self) -> None:
        """Сохранение изменённых полей заявки (модель, описание, запчасти)"""
        car_model = self.entry_car_model.get().strip() if hasattr(self, "entry_car_model") else ""
        problem = self.text_problem.get("1.0", tk.END).strip() if hasattr(self, "text_problem") else ""
        parts = self.entry_parts.get().strip() if hasattr(self, "entry_parts") else ""

        if not car_model:
            messagebox.showwarning("Ошибка ввода", "Поле 'Модель' не может быть пустым.")
            return
        if not problem:
            messagebox.showwarning("Ошибка ввода", "Поле 'Описание проблемы' не может быть пустым.")
            return

        if update_request_details(self.request_id, car_model, problem, parts):
            messagebox.showinfo("Успех", "Данные заявки обновлены.")
            # Зафиксировать новые значения как оригинальные и выключить режим редактирования
            self._orig_car_model = car_model
            self._orig_problem = problem
            self._orig_parts = parts
            self._disable_edit_mode()
        else:
            messagebox.showerror("Ошибка", "Не удалось обновить заявку.")

    def _enable_edit_mode(self) -> None:
        if hasattr(self, "entry_car_model"):
            self.entry_car_model.configure(state="normal")
        if hasattr(self, "text_problem"):
            self.text_problem.configure(state="normal")
        if hasattr(self, "entry_parts"):
            self.entry_parts.configure(state="normal")
        if hasattr(self, "btn_save_details"):
            self.btn_save_details.configure(state="normal")
        if hasattr(self, "btn_cancel_details"):
            self.btn_cancel_details.configure(state="normal")

    def _disable_edit_mode(self) -> None:
        if hasattr(self, "entry_car_model"):
            self.entry_car_model.configure(state="disabled")
        if hasattr(self, "text_problem"):
            self.text_problem.configure(state="disabled")
        if hasattr(self, "entry_parts"):
            self.entry_parts.configure(state="disabled")
        if hasattr(self, "btn_save_details"):
            self.btn_save_details.configure(state="disabled")
        if hasattr(self, "btn_cancel_details"):
            self.btn_cancel_details.configure(state="disabled")

    def _cancel_edit_mode(self) -> None:
        # Вернуть исходные значения
        if hasattr(self, "entry_car_model"):
            self.entry_car_model.configure(state="normal")
            self.entry_car_model.delete(0, tk.END)
            self.entry_car_model.insert(0, getattr(self, "_orig_car_model", ""))
            self.entry_car_model.configure(state="disabled")
        if hasattr(self, "text_problem"):
            self.text_problem.configure(state="normal")
            self.text_problem.delete("1.0", tk.END)
            self.text_problem.insert("1.0", getattr(self, "_orig_problem", ""))
            self.text_problem.configure(state="disabled")
        if hasattr(self, "entry_parts"):
            self.entry_parts.configure(state="normal")
            self.entry_parts.delete(0, tk.END)
            self.entry_parts.insert(0, getattr(self, "_orig_parts", ""))
            self.entry_parts.configure(state="disabled")
        if hasattr(self, "btn_save_details"):
            self.btn_save_details.configure(state="disabled")
        if hasattr(self, "btn_cancel_details"):
            self.btn_cancel_details.configure(state="disabled")

    def _assign_master(self) -> None:
        idx = self.combo_master.current()
        master_id = self.master_ids[idx] if 0 <= idx < len(self.master_ids) else None
        if update_request_master(self.request_id, master_id):
            self.current_master_id = master_id
            messagebox.showinfo("Успех", "Механик назначен.")
        else:
            messagebox.showerror("Ошибка", "Не удалось назначить механика.")

    def _add_comment(self) -> None:
        msg = self.entry_comment.get().strip()
        if not msg:
            messagebox.showwarning("Ошибка", "Введите текст комментария.")
            return
        if add_comment(self.request_id, self.user.user_id, msg):
            self.entry_comment.delete(0, tk.END)
            self._fill_comments()
            messagebox.showinfo("Успех", "Комментарий добавлен.")
        else:
            messagebox.showerror("Ошибка", "Не удалось добавить комментарий.")

    def _delete_request(self) -> None:
        if not messagebox.askyesno("Подтверждение", "Удалить эту заявку? Действие нельзя отменить."):
            return
        if delete_request(self.request_id):
            messagebox.showinfo("Успех", "Заявка удалена.")
            self._on_close()
        else:
            messagebox.showerror("Ошибка", "Не удалось удалить заявку.")

    def _show_qr(self) -> None:
        """Генерация QR-кода для опроса качества (Модуль 3)"""
        if not QR_CODE_AVAILABLE:
            messagebox.showerror("Ошибка", "Библиотека для QR-кода недоступна.")
            return
        
        try:
            qr = qrcode.make(QUALITY_SURVEY_URL)
            path = f"qr_code_{self.request_id}.png"
            qr.save(path)
        except Exception as exc:
            messagebox.showerror("Ошибка", f"Не удалось создать QR-код: {exc}")
            return
        
        win = tk.Toplevel(self.root)
        win.title("QR-код для отзыва")
        img = ImageTk.PhotoImage(Image.open(path))
        lbl = tk.Label(win, image=img)
        lbl.image = img
        lbl.pack(padx=10, pady=10)
        tk.Label(win, text="Отсканируйте для оценки качества работы", font=("Arial", 10)).pack(pady=5)

    def _on_close(self) -> None:
        self.on_close()
        self.root.destroy()


class StatisticsForm:
    """Форма статистики работы сервиса"""
    
    def __init__(self, root: tk.Toplevel) -> None:
        self.root = root
        self.root.title("Статистика — АвтоТранс")
        self.root.geometry("640x560")
        self.root.config(bg=BG_COLOR)
        
        self._build_header()
        self._build_content()

    def _build_header(self) -> None:
        header = tk.Frame(self.root, bg=HEADER_BG, height=48)
        header.pack(fill="x")
        tk.Label(header, text="📊 Статистика", fg=HEADER_FG, 
                 bg=HEADER_BG, font=(FONT_FAMILY, 12)).pack(side="left", padx=PAD * 2, pady=12)
        tk.Button(header, text="Назад", fg=HEADER_FG, bg=HEADER_BG, 
                  font=(FONT_FAMILY, 10), relief="flat", cursor="hand2", 
                  command=self.root.destroy).pack(side="right", padx=PAD * 2, pady=10)

    def _build_content(self) -> None:
        content = tk.Frame(self.root, bg=BG_COLOR, padx=PAD * 2, pady=PAD * 2)
        content.pack(fill="both", expand=True)
        
        tk.Label(content, text="Статистика работы сервиса", 
                 font=(FONT_FAMILY, 14, "bold"), bg=BG_COLOR).pack(pady=(0, PAD))
        
        card = tk.Frame(content, bg=CARD_BG, padx=PAD * 2, pady=PAD * 2)
        card.pack(fill="x", pady=PAD)
        
        completed = get_completed_requests_count()
        avg_time = get_average_repair_time()
        all_reqs = get_all_requests()
        total = len(all_reqs)
        new_count = sum(1 for r in all_reqs if r.request_status == "Новая заявка")
        in_progress = sum(1 for r in all_reqs if r.request_status == "В процессе ремонта")
        
        tk.Label(card, text=f"Всего заявок: {total}", font=(FONT_FAMILY, 11), bg=CARD_BG).pack(anchor="w", pady=4)
        tk.Label(card, text=f"Выполнено (готова к выдаче): {completed}", font=(FONT_FAMILY, 11), bg=CARD_BG).pack(anchor="w", pady=4)
        tk.Label(card, text=f"Активные (в работе): {total - completed}", font=(FONT_FAMILY, 11), bg=CARD_BG).pack(anchor="w", pady=4)
        tk.Label(card, text=f"Новые: {new_count} · В процессе ремонта: {in_progress}", font=(FONT_FAMILY, 11), bg=CARD_BG).pack(anchor="w", pady=4)
        
        if avg_time > 0:
            tk.Label(card, text=f"Среднее время ремонта: {avg_time} дн.", font=(FONT_FAMILY, 11), bg=CARD_BG).pack(anchor="w", pady=4)
        else:
            tk.Label(card, text="Среднее время ремонта: нет завершённых заявок", 
                     font=(FONT_FAMILY, 11), fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w", pady=4)
        
        tk.Label(content, text="Топ-5 типов неисправностей", 
                 font=(FONT_FAMILY, 11, "bold"), bg=BG_COLOR).pack(anchor="w", pady=(PAD, 4))
        
        top_card = tk.Frame(content, bg=CARD_BG, padx=PAD * 2, pady=PAD * 2)
        top_card.pack(fill="x")
        
        counts = {}
        for r in all_reqs:
            desc = (r.problem_descryption or "").strip()
            if desc:
                counts[desc] = counts.get(desc, 0) + 1
        
        if not counts:
            tk.Label(top_card, text="Данных нет.", font=(FONT_FAMILY, 10), fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w")
        else:
            for i, (desc, cnt) in enumerate(sorted(counts.items(), key=lambda x: -x[1])[:5], 1):
                tk.Label(top_card, text=f"{i}. {desc} ({cnt})", font=(FONT_FAMILY, 10), bg=CARD_BG).pack(anchor="w", pady=2)