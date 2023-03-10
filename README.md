# YaMDB project

![workflow](https://github.com/ltlrn/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число).
Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).
На одно произведение пользователь может оставить только один отзыв.  

Проект развернут, админка доступена по адресу: 

http://51.250.72.4/admin/login/?next=/admin/
  
## Технологии
- Python 3.7+  
- Django 2.2.16  
- Django rest framework 3.12.4
- Postgres
- Docker
### Документация и возможности API:
К проекту подключен redoc. Для просмотра документации используйте эндпойнт `redoc/`

### Запуск:

- Склонируйте репозитрий на свой компьютер
- Создайте `.env` файл в директории `infra/`, в котором должны содержаться следующие переменные:
    >DB_ENGINE=django.db.backends.postgresql\
    >DB_NAME= # название БД\ 
    >POSTGRES_USER= # ваше имя пользователя\
    >POSTGRES_PASSWORD= # пароль для доступа к БД\
    >DB_HOST=db\
    >DB_PORT=5432\
- Из папки `infra/` соберите образ при помощи docker-compose
`$ docker-compose up -d --build`
- Примените миграции
`$ docker-compose exec web python manage.py migrate`
- Соберите статику
`$ docker-compose exec web python manage.py collectstatic --no-input`
- Создайте суперюзера
`$ docker-compose exec web python manage.py createsuperuser`

## Авторы проекта
Роберт Левченко  
Дмитрий Сухарев  
Алексей Тарасов