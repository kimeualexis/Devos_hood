from django import forms
from .models import Comment, Question


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'image']
