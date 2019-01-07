from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Question, Comment

"""
def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})
    """


class QuestionListView(ListView):
    model = Question
    template_name = 'quiz/index.html'
    context_object_name = 'questions'
    ordering = ['-created']
    paginate_by = 2


class UserQuestionListView(ListView):
    model = Question
    template_name = 'quiz/user_questions.html'
    context_object_name = 'questions'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Question.objects.filter(author=user).order_by('-created')


class QuestionDetailView(DetailView):
    model = Question


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question

    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


"""
class CommentListView(ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = ''
    """


class CommentCreateView(CreateView):
    model = Comment
    fields = ['comment', 'image']

    """
    def get_success_url(self):
        return reverse('blog:post-detail')
        """

    def form_valid(self, form, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        form.instance.author = self.request.user
        form.instance.question = question
        # form.instance.post = self.request.post
        return super(CommentCreateView, self).form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment

    fields = ['comment', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


def about(request):
    return render(request, 'quiz/about.html')
