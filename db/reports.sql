

-- 1. Все активные заявки (в работе)
SELECT 
    r.requestID,
    r.startDate,
    r.carModel,
    r.problemDescryption,
    u.fio AS client,
    m.fio AS master
FROM Requests r
LEFT JOIN Users u ON r.clientID = u.userID
LEFT JOIN Users m ON r.masterID = m.userID
WHERE r.requestStatus = 'В процессе ремонта';

-- 2. Статистика по механикам
SELECT 
    m.fio AS mechanic,
    COUNT(r.requestID) AS total_requests,
    SUM(CASE WHEN r.requestStatus = 'Готова к выдаче' THEN 1 ELSE 0 END) AS completed
FROM Users m
LEFT JOIN Requests r ON m.userID = r.masterID
WHERE m.type = 'Автомеханик'
GROUP BY m.userID, m.fio;

-- 3. Просроченные заявки (ремонт > 14 дней)
SELECT 
    r.requestID,
    r.startDate,
    r.carModel,
    julianday('now') - julianday(r.startDate) AS days_in_repair,
    m.fio AS master
FROM Requests r
LEFT JOIN Users m ON r.masterID = m.userID
WHERE r.requestStatus != 'Готова к выдаче'
  AND julianday('now') - julianday(r.startDate) > 14;

-- 4. Топ-5 неисправностей
SELECT 
    problemDescryption,
    COUNT(*) AS count
FROM Requests
GROUP BY problemDescryption
ORDER BY count DESC
LIMIT 5;

-- 5. Заявки конкретного клиента
SELECT 
    r.requestID,
    r.startDate,
    r.carModel,
    r.requestStatus,
    r.completionDate
FROM Requests r
WHERE r.clientID = 7
ORDER BY r.startDate DESC;

-- 6. Комментарии по заявке
SELECT 
    c.createdDate,
    u.fio AS author,
    c.message
FROM Comments c
JOIN Users u ON c.masterID = u.userID
WHERE c.requestID = 1
ORDER BY c.createdDate DESC;