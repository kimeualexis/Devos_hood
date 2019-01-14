from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Question, Comment
from .forms import CommentForm, QuestionForm


class QuestionListView(LoginRequiredMixin, ListView):
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
    success_url = '/home'

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


class CommentCreateView(CreateView):
    model = Comment
    fields = ['comment']

    def get_success_url(self):
        return reverse('quiz:question-detail', kwargs={'pk': self.get_object(Question.objects.all()).pk})

        pass

    def form_valid(self, form, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        form.instance.author = self.request.user
        form.instance.question = question
        return super(CommentCreateView, self).form_valid(form)


def detail(request, quiz_id):
    quiz = get_object_or_404(Question, pk=quiz_id)
    return render(request, 'quiz/question_detail.html', {'quiz': quiz})
  
  
def create_quiz(request):
    form = QuestionForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        question = form.save(commit=False)
        question.author = request.user
        question.image = request.FILES['image']
        question.save()
    return render(request, 'quiz/question_form.html', {'form': form})
    
"""


def detail(request, quiz_id):
    form = CommentForm(request.POST or None, request.FILES or None)
    quiz = get_object_or_404(Question, pk=quiz_id)
    if form.is_valid():
        comm = form.save(commit=False)
        comm.author = request.user
        # comm.image = request.FILES['image']
        comm.question = quiz
        comm.save()
    form = CommentForm()
    return render(request, 'quiz/question_detail.html', {'form': form, 'quiz': quiz})


def delete(request, quiz_id):
    quiz = get_object_or_404(Question, pk=quiz_id)
    quiz.delete()
    return redirect('quiz:quiz-index')


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


"""
def delete_comment(request, quiz_id, comment_id):
    quiz = get_object_or_404(Question, pk=quiz_id)
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    return render(request, 'quiz/question_detail.html', {'quiz': quiz})
    """
