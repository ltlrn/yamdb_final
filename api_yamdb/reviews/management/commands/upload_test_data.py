import csv
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from api_yamdb.settings import BASE_DIR

DATA_DIR = os.path.join(BASE_DIR, 'static/data/')
User = get_user_model()


class Command(BaseCommand):
    help = 'Заливает тестовые данные из csv файлов в папке static/data'

    def upload_genre_titles_csv_to_SQL(self):
        """Заливка из genre_title.csv напрямую в SQL таблицу title_genres."""
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM title_genres")
            row_count = cursor.fetchone()[0]
            if row_count == 0:
                file_path = os.path.join(DATA_DIR, 'genre_title.csv')
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        sql_stmt = "INSERT INTO title_genres VALUES (%s,%s,%s)"
                        params = (row['id'], row['title_id'], row['genre_id'])
                        cursor.execute(sql_stmt, [*params])
                    cursor.execute("SELECT COUNT(*) FROM title_genres")
                    row_count = cursor.fetchone()[0]
                    msg = f'Залито записей в title_genre: {row_count}'
                    self.stdout.write(msg)
            else:
                msg = 'Таблица title_genres не пуста, заливка csv отменена'
                self.stdout.write(msg)

    def handle(self, *args, **options):
        try:
            from reviews.models import Category, Comments, Genre, Review, Title
            self.stdout.write('Модели Category/Genre/Title/Review/Comments ок')
            FILES_AND_MODELS = (
                ('users.csv', User),
                ('category.csv', Category),
                ('genre.csv', Genre),
                ('titles.csv', Title),
                ('review.csv', Review),
                ('comments.csv', Comments),
            )
            for file, class_name in FILES_AND_MODELS:
                file_path = os.path.join(DATA_DIR, file)
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    counter = 0
                    for row in reader:
                        if class_name == Title:
                            cat_id = row['category']
                            row['category'] = Category.objects.get(id=cat_id)
                        if class_name == Review:
                            title_id = row['title_id']
                            row['title'] = Title.objects.get(id=title_id)
                            author_id = row['author']
                            row['author'] = User.objects.get(id=author_id)
                        if class_name == Comments:
                            review_id = row['review_id']
                            row['review'] = Review.objects.get(id=review_id)
                            author_id = row['author']
                            row['author'] = User.objects.get(id=author_id)
                        class_name.objects.update_or_create(
                            id=row['id'], defaults=row)
                        counter += 1
                msg = f'Залито объектов {class_name.__name__}: {counter}'
                self.stdout.write(msg)
        except ImportError:
            raise CommandError('Не могу импортировать нужные модели')
        except FileNotFoundError:
            raise CommandError('Как минимум один из csv файлов отсутствует!')

        self.upload_genre_titles_csv_to_SQL()
