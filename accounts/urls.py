from django.contrib.auth import views
from django.urls import path, include
from accounts import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('contact', views.contact_form, name="contact"),
    path('register/', views.Register.as_view(), name='register'),
    path('update_profil/', views.UpdateProfile.as_view(), name='update_profile'),
    path('my_profile/', cache_page(60*10)(views.UserProfile.as_view()), name='my_profile'),

    path('posts/', cache_page(60*10)(views.PostListView.as_view()), name='post-list'),
    path('posts/<int:pk>', cache_page(60*10)(views.PostDetailView.as_view()), name='post-detail'),
    path('posts/create', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete', views.PostDeleteView.as_view(), name='post-delete'),

    path('authors/', views.AuthorsListView.as_view(), name='authors-list'),
    path('authors/<int:pk>', views.view_user_profile, name='authors-detail'),

    path('comments/', views.CommentListView.as_view(), name='comment-list'),
    path('comments/<int:pk>', cache_page(60*10)(views.CommentDetailView.as_view()), name='comment-detail'),

    path('posts/<int:pk>/create_comment/', views.CommentCreateView.as_view(), name='comment-create'),
    path('posts_update/', views.PostUpdateListView.as_view(), name='post_update-list'),
    path('posts_update/<int:pk>', views.PostUpdateDetailView.as_view(), name='post-detail-update'),

    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complet'),
]
