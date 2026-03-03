

-- Таблица: Пользователи системы
CREATE TABLE IF NOT EXISTS Users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    fio TEXT NOT NULL,
    phone TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN (
        'Менеджер', 
        'Менеджер по качеству', 
        'Оператор', 
        'Автомеханик', 
        'Заказчик'
    ))
);

-- Таблица: Заявки на ремонт
CREATE TABLE IF NOT EXISTS Requests (
    requestID INTEGER PRIMARY KEY AUTOINCREMENT,
    startDate TEXT NOT NULL,
    carType TEXT NOT NULL CHECK(carType IN ('Легковая', 'Грузовая', 'Внедорожник')),
    carModel TEXT NOT NULL,
    problemDescryption TEXT NOT NULL,
    requestStatus TEXT DEFAULT 'Новая заявка' 
        CHECK(requestStatus IN ('Новая заявка', 'В процессе ремонта', 'Готова к выдаче')),
    completionDate TEXT,
    repairParts TEXT,
    masterID INTEGER,
    clientID INTEGER NOT NULL,
    
    FOREIGN KEY (masterID) REFERENCES Users(userID) ON DELETE SET NULL,
    FOREIGN KEY (clientID) REFERENCES Users(userID) ON DELETE CASCADE
);

-- Таблица: Комментарии к заявкам
CREATE TABLE IF NOT EXISTS Comments (
    commentID INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    masterID INTEGER NOT NULL,
    requestID INTEGER NOT NULL,
    createdDate TEXT DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (masterID) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (requestID) REFERENCES Requests(requestID) ON DELETE CASCADE
);

-- Индексы для ускорения поиска
CREATE INDEX IF NOT EXISTS idx_requests_status ON Requests(requestStatus);
CREATE INDEX IF NOT EXISTS idx_requests_client ON Requests(clientID);
CREATE INDEX IF NOT EXISTS idx_requests_master ON Requests(masterID);
CREATE INDEX IF NOT EXISTS idx_comments_request ON Comments(requestID);