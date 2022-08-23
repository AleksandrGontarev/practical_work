from django.contrib.auth import views
from django.urls import path, include
from accounts import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.Register.as_view(), name='register'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/create', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete', views.PostDeleteView.as_view(), name='post-delete'),
    path('users/', views.UsersListView.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('comments/', views.CommentListView.as_view(), name='comment-list'),
    path('comments/<int:pk>', views.CommentDetailView.as_view(), name='comment-detail'),
    path('posts/<int:pk>/create_comment/', views.CommentCreateView.as_view(), name='comment-create'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complet'),
]
