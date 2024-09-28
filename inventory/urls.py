from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ItemView,UserView

urlpatterns = [
    path('items/', ItemView.as_view()),
    path('createusers/', UserView.as_view()),
    path('items/<int:item_id>/', ItemView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
