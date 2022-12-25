from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ConfCodeSerializer
from .views import mail_code

urlpatterns = [
    path('signup/', mail_code),
    path(
        'token/',
        TokenObtainPairView.as_view(serializer_class=ConfCodeSerializer),
        name='token_obtain_pair',
    ),
]
