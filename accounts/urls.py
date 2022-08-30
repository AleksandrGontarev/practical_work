from django.urls import path, include
from accounts import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('contact', views.contact_form, name="contact"),
    path('register/', views.Register.as_view(), name='register'),
    path('update_profil/', views.UpdateProfile.as_view(), name='update_profile'),
    path('my_profile/', views.UserProfile.as_view(), name='my_profile'),

    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/create', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete', views.PostDeleteView.as_view(), name='post-delete'),

    path('authors/', views.AuthorsListView.as_view(), name='authors-list'),
    path('authors/<int:pk>', views.view_user_profile, name='authors-detail'),

    path('comments/', views.CommentListView.as_view(), name='comment-list'),
    path('comments/<int:pk>', views.CommentDetailView.as_view(), name='comment-detail'),

    path('posts/<int:pk>/create_comment/', views.CommentCreateView.as_view(), name='comment-create'),
    path('posts_update/', views.PostUpdateListView.as_view(), name='post_update-list'),
    path('posts_update/<int:pk>', views.PostUpdateDetailView.as_view(), name='post-detail-update'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
