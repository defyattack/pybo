from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,UserModel
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model  # helper 함수를 통해 모델 클래스 참고


class UserBasicForm(forms.ModelForm):
    username = forms.CharField(label="사용자ID")
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("email",)


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "email")


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(label="이메일")
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ("username", "email")


"""
class PassUpdateForm(forms.ModelForm):
    password1 = forms.CharField(label='새 비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='새 비밀번호 확인', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username",)
"""
