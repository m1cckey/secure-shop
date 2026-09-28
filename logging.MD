# Стандарт хранения информации
access.log: Apache combined
* access.log: json
    - IP: ip клиента
    - timestamp: ISO 8601
    - username: username из формы 
    - latency_ms: длительность в милимекундах
    - result: результат (success, invalid_username, invalid_password)
* auth.log: 
    - удачный логин
    - неудачный логин
    - регистрация
    - выход из акккаунта