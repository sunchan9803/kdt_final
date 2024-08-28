from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Pboard, Pcomment

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'email']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class PboardForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('recommendation', '추천'),
        ('chat', '사담'),
        ('review', '후기'),
        ('transport', '교통정보'),
        ('restaurant', '근처 맛집'),
        ('other', '기타'),
    ]

    FONT_SIZE_CHOICES = [
        ('16px', '16px'),
        ('18px', '18px'),
        ('20px', '20px'),
        ('22px', '22px'),
        ('24px', '24px'),
    ]

    FONT_FAMILY_CHOICES = [
        ('Hahmlet', 'Hahmlet'),
        ('Orbit', 'Orbit'),
        ('Dongle', 'Dongle'),
        ('Jua', 'Jua'),
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    title = forms.CharField(max_length=200)
    content = forms.CharField(widget=forms.Textarea)
    font_size = forms.ChoiceField(choices=FONT_SIZE_CHOICES)
    font_family = forms.ChoiceField(choices=FONT_FAMILY_CHOICES)  # 폼에 font_family 필드 추가

    class Meta:
        model = Pboard
        fields = ['category', 'title', 'content', 'font_size', 'font_family']

class PcommentForm(forms.ModelForm):
    class Meta:
        model = Pcomment
        fields = ['content']  # 댓글 내용만 입력 받음
