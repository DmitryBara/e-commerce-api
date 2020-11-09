from django.urls import path
from .views import ProfileDetail, ProfileList, SubscribeDetail

# /api/userprofile/
urlpatterns = [
    path('create/', ProfileDetail.as_view()),
    path('<int:profile_id>/', ProfileDetail.as_view()),
    path('all/', ProfileList.as_view()),
    path('subscribe/', SubscribeDetail.as_view()),
]