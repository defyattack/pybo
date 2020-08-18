from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('user_mod/', views.user_mod, name='user_mod'),
    path('pass_mod_p/', views.pass_mod_p, name='pass_mod_p'),
    path('pass_mod_req/', views.pass_mod_req, name='pass_mod_req'),
    path('user_info/', views.user_info, name='user_info'),
]