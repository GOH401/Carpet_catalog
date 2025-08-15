# Carpet Catalog

Веб-приложение для управления каталогом ковров с поддержкой загрузки изображений в Supabase Storage и деплоем на Railway.  
Проект создан для компании Bal Tekstil в рамках цифровой трансформации и оптимизации процессов.

## Демоверсия
[Открыть демо](https://catalognew-production.up.railway.app/) 


## Стек технологий
- Backend: Python, Django, Django ORM, PostgreSQL
- Frontend: Bootstrap 5, JavaScript
- Хранение файлов: Supabase Storage
- Деплой: Railway
- Прочее: GitHub Actions (CI), .env конфигурация

## Возможности
- CRUD-операции с карточками ковров  
- Загрузка и отображение изображений через Supabase Storage  
- Поиск и фильтрация по характеристикам  
- Адаптивный дизайн на Bootstrap 5  
- Ролевая модель доступа (админ / менеджер)

## Локальный запуск
```bash
# Клонируем проект
git clone https://github.com/GOH401/Carpet_catalog.git
cd Carpet_catalog

# Создаём и активируем виртуальное окружение
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Настраиваем .env (пример в .env.example)
cp .env.example .env

# Применяем миграции и запускаем сервер
python manage.py migrate
python manage.py runserver