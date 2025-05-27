from django.urls import path
from rest_framework.routers import DefaultRouter
from habits.apps import HabitsConfig
from habits.views import HabitsViewSet, UserHabitViewSet, PublishedHabitListAPIView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r"habits", HabitsViewSet, basename="habits")

urlpatterns = [
    path("user-habits-list/", UserHabitViewSet.as_view(), name="user-habits-list"),
    path("published-habits-list/", PublishedHabitListAPIView.as_view(), name="published-habits-list"),
] + router.urls
