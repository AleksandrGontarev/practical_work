from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreationForm, ContactFrom
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth import authenticate, login
from .models import Post, Comment, User
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import MultipleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from .tasks import send_mail as celery_send_mail
from .tasks import send_mail_to_user


def contact_form(request):
    if request.method == "POST":
        form = ContactFrom(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            celery_send_mail.delay(subject, message, from_email)
            messages.add_message(request, messages.SUCCESS, 'Message sent')
            return redirect('contact')
    else:
        form = ContactFrom()
    return render(
        request,
        "accounts/contact.html",
        context={
            "form": form,
        }
    )


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {'form': UserCreationForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {'form': form}
        return render(request, self.template_name, context)


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name = 'registration/update_profile.html'
    success_url = reverse_lazy("my_profile")
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UserProfile(LoginRequiredMixin, DetailView):
    model = User
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class AuthorsListView(ListView):
    model = User
    paginate_by = 2
    template_name = 'accounts/authors_list.html'


# def get_user_profile(request, pk):
#     user = User.objects.get(pk=pk)
#     return render(request, 'accounts/authors.html', {"user": user})


# class AuthorsDetailView(DetailView):
#     model = User
#     template_name = 'accounts/authors.html'


def view_user_profile(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'accounts/authors.html', {
        'profile': user
    })


class PostDetailView(DetailView):
    model = Post
    paginate_by = 2

    def get_context_data(self, **kwargs):
        object_list = Comment.objects.filter(posts=self.get_object())
        context = super(PostDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context
    # def get_context_data(self, **kwargs):
    #     object_list = self.object.comment_set.filter(posts=self.get_object())
    #     context = super(PostDetailView, self).get_context_data(object_list=object_list, **kwargs)
    #     return context


class PostListView(ListView):
    model = Post
    paginate_by = 2
    ordering = ['title']
    queryset = Post.objects.select_related('author').prefetch_related('comment_set')


class PostUpdateDetailView(DetailView):
    model = Post
    paginate_by = 2
    template_name = 'accounts/post_update_detail.html'


class PostUpdateListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 2
    ordering = ['title']
    template_name = 'accounts/post_update_list.html'
    queryset = Post.objects.select_related('author')

    def get_context_data(self, **kwargs):
        object_list = Post.objects.filter(author=self.request.user)
        context = super(PostUpdateListView, self).get_context_data(object_list=object_list, **kwargs)
        return context
    # def get_queryset(self, *args, **kwargs):
    #     return super.get_queryset(*args, **kwargs).filter(
    #         owner=self.request.user
    #     )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'short_description', 'full_description', 'image', 'data_post']

    def form_valid(self, form):
        subjects = form.cleaned_data.get('author')
        message = "New post:{title}\n short description: {short}".format(title=form.cleaned_data.get('title'),
                                                                         short=form.cleaned_data.get(
                                                                             'short_description'))
        celery_send_mail.delay(subject=subjects, message=message, from_email='my-blog@gmail.com')
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'title', 'short_description', 'full_description', 'image', 'data_post']
    template_name = "accounts/post_update.html"

    def get_context_data(self, **kwargs):
        object_list = Post.objects.filter(author=self.request.user)
        context = super(PostUpdateView, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def form_valid(self, form):
        form.instance.posts = Post.objects.get(pk=self.kwargs['pk'])
        return super(PostUpdateView, self).form_valid(form)


class PostDeleteView(DeleteView):
    pass
    # model = Post
    # success_url = reverse_lazy("book_store:author-list")
    # success_message = 'Author Delete Successfully'
    # template_name = "book_store/author_delete.htm


class CommentListView(ListView):
    model = Comment
    paginate_by = 2
    ordering = ['text_comment']
    queryset = Comment.objects.select_related('posts')


class CommentDetailView(DetailView):
    model = Comment
    paginate_by = 2


class CommentCreateView(CreateView):
    model = Comment
    fields = ['username', 'text_comment']

    def form_valid(self, form):
        post = str(Post.objects.get(pk=self.kwargs['pk']))
        subjects = form.cleaned_data.get('username')
        message = "New comment:{text}\n for post_title: {post}".format(text=form.cleaned_data.get('text_comment'),
                                                                       post=post)
        celery_send_mail.delay(subject=subjects, message=message, from_email='my-blog@gmail.com')

        send_mail_to_user.delay(subject=subjects, message=post)

        form.instance.posts = Post.objects.get(pk=self.kwargs['pk'])
        return super(CommentCreateView, self).form_valid(form)
