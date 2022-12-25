from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from .views import CategoryViewSet, GenreViewSet, TitleDetail, TitleList
from .views import CommentsViewSet, ReviewViewSet

router_1 = DefaultRouter()
router_1.register('v1/categories', CategoryViewSet)
router_1.register('v1/genres', GenreViewSet)
router_1.register("v1/users", UserViewSet)
router_1.register(r'v1/titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                  basename='reviews')
router_1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments')

urlpatterns = [
    path('', include(router_1.urls)),
    path('v1/titles/', TitleList.as_view(), name='title-list'),
    path('v1/titles/<int:pk>/', TitleDetail.as_view(), name='title-detail'),
]
