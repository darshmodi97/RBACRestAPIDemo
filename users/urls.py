from django.urls import path
from users import views
app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('', views.UserListView.as_view(), name='user_list'),
    path('<int:pk>/profile/', views.ShowProfile.as_view(), name='show_profile'),
    path('update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("<int:pk>/delete/", views.DeleteView.as_view(), name="delete")
]
