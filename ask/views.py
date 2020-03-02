from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.db.models import Q
from django import forms
from .models import Question, Comment, Reply
from django.utils import timezone
from .forms import CommentCreateForm, ReplyCreateForm, QuestionCreateForm, QuestionSearchForm, SignUpForm

# Create your views here.
class HomeView(generic.TemplateView):
    template_name = 'ask/home.html'

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('ask:login')
    template_name = 'ask/signup_form.html'


class QuestionList(ListView):
    model = Question
    paginate_by = 10
    template_name = 'ask/question_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = QuestionSearchForm(self.request.GET or None)
        if form.is_valid():
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                for word in key_word.split():
                    queryset = queryset.filter(Q(title__icontains=word) | Q(question__icontains=word))
        
        queryset = queryset.order_by('-posted_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = QuestionSearchForm(self.request.GET or None)
        return context


class Question_Detail(generic.DetailView):
    model = Question
    template_name = 'ask/question_detail.html'

    # rewrite this with after user functions are done 
    def get_object(self, queryset=None):
        question = super().get_object()
        return question

class CommentCreation(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = 'ask/comment_form.html'
    success_url = reverse_lazy('ask:question_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        question_pk = self.kwargs['pk']
        question = get_object_or_404(Question, pk=question_pk)
        comment = form.save(commit=False)
        comment.post = question
        comment.save()
        return redirect('ask:question_detail', pk=question_pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Question, pk=self.kwargs['pk'])
        return context

class ReplyCreation(LoginRequiredMixin, generic.CreateView):
    model = Reply
    form_class = ReplyCreateForm
    template_name = 'ask/comment_form.html'
    success_url = reverse_lazy('ask:question_list')
    
    def form_valid(self, form):
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)
        reply = form.save(commit=False)
        reply.target = comment
        reply.save()
        return redirect('ask:question_detail', pk=comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)
        context['question'] = comment.post
        return context

class QuestionPost(LoginRequiredMixin, generic.CreateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'ask/question_form.html'
    success_url = reverse_lazy('ask:question_list')
