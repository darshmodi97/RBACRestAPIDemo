from django.urls import path
from users import views
app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('', views.UserListView.as_view(), name='user_list'),
    path('<int:pk>/profile/', views.ShowProfile.as_view(), name='show_profile')
]
