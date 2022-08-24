from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Post, Comment

User = get_user_model()


class PostInline(admin.StackedInline):
    model = Post
    extra = 1


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [PostInline, ]
    list_filter = ['username', 'last_name', ]
    search_fields = ['username', 'last_name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'short_description', 'full_description', 'image')
    inlines = [CommentInline, ]
    list_filter = ['title', 'author']
    search_fields = ['title', 'author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'text_comment', 'posts')
    list_filter = ['username']
    search_fields = ['username']


# admin.site.register(Post)

# admin.site.register(Comment)

