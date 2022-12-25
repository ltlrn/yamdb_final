from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class SimpleSlugModelTemplate(models.Model):
    """Шаблон для создания простых моделей со Slug-ом."""
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True)

    class Meta():
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:20]


class Category(SimpleSlugModelTemplate):
    """Категории произведений."""

    class Meta(SimpleSlugModelTemplate.Meta):
        verbose_name_plural = 'Категории'


class Genre(SimpleSlugModelTemplate):
    """Жанры произведений."""

    class Meta(SimpleSlugModelTemplate.Meta):
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведения (книги, фильмы, музыка и пр.)."""
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год')
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        db_table='title_genres',
        verbose_name='Жанр'
    )

    class Meta():
        ordering = ('name',)
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:30]


class Review(models.Model):
    """Отзывы пользователей и их оценки произведений"""
    text = models.TextField(verbose_name='Отзыв')
    score = models.IntegerField(
        verbose_name='Пользовательская оценка',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]
        verbose_name_plural = 'Отзывы'


class Comments(models.Model):
    """Комментарии пользователей к отзывам"""
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Комментарии'
