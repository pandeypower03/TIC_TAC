from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, GameViewSet, UserProfileViewSet, UserListView, MatchHistoryView

router = DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('match-history/', MatchHistoryView.as_view(), name='match-history'),
]
