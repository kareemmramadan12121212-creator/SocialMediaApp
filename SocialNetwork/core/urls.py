from django.urls import path
from .views import *
urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('account_settings/', AccountSettingsView.as_view(), name='settings'),
    path('add-post/', AddPost.as_view(), name='addpost'),
    path('user/<str:username>/', UserProfile.as_view(), name='username'),
    path('search/', SearchUsers.as_view(), name='search'),
    path('follow/<int:id>', follow_user, name='follow'),
    path('unfollow/<int:id>', unfollow_user, name='unfollow'),
    path('home/', HomePage.as_view(), name='HomePage'),
]