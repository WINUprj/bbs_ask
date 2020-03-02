from .models import Question, Comment, Reply
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('post',)
        widgets = {
            'text': forms.Textarea(
                attrs={'placeholder': 'Write down the comment'}
            )
        }

class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Reply
        exclude = ('target', 'created_at',)
        widgets = {
            'text': forms.Textarea(
                attrs={'placeholder': 'Reply to the comment'}
            )
        }

class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('updated_date', 'posted_date',)
        widgets = {
            'question': forms.Textarea(
                attrs={'placeholder': 'Ask your question!'}
            )
        }

class QuestionSearchForm(forms.Form):
    key_word = forms.CharField(
        label='検索',
        required=False
    )

class SignUpForm(auth_forms.UserCreationForm):
    username = forms.CharField(max_length=20, required=True, help_text='Required field')
    email = forms.CharField(max_length=254, required=True, help_text='Required field')

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2', 'first_name', 'last_name'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード（確認）'
        self.fields['first_name'].widget.attrs['placeholder'] = '名前'
        self.fields['last_name'].widget.attrs['placeholder'] = '苗字'
    


class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
        self.fields['password'].widget.attrs['placeholder'] = 'パスワード'