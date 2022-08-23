from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from .models import Post, Comment, User
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import MultipleObjectMixin


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


class PostDetailView(DetailView, MultipleObjectMixin):
    model = Post
    paginate_by = 2
    # queryset = Post.objects.prefetch_related('comment_set')

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
    # queryset = Post.objects.select_related("author")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'title', 'short_description', 'full_description', 'image', 'data_post']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    pass
    # model = Post
    # fields = ['name', 'age']
    # template_name = "book_store/author_update.html"


class PostDeleteView(DeleteView):
    pass
    # model = Post
    # success_url = reverse_lazy("book_store:author-list")
    # success_message = 'Author Delete Successfully'
    # template_name = "book_store/author_delete.htm


class UsersListView(ListView):
    model = User
    paginate_by = 2


class UserDetailView(DetailView):
    model = User


class CommentListView(ListView):
    model = Comment
    paginate_by = 2
    ordering = ['text_comment']
    # queryset = Comment.objects.select_related('posts')


class CommentDetailView(DetailView):
    model = Comment
    paginate_by = 2


class CommentCreateView(CreateView):
    model = Comment
    fields = ['username', 'text_comment']

    def form_valid(self, form):
        form.instance.posts = Post.objects.get(pk=self.kwargs['pk'])
        return super(CommentCreateView, self).form_valid(form)



