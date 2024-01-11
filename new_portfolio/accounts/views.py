from django.shortcuts import render, redirect
from .forms import RegistForm
from django.core.exceptions import ValidationError
from .models import UserActivateTokens

# Create your views here.

def home(request):
    return render(
        request, 'accounts/home.html'
    )

def regist(request):
    regist_form = RegistForm(request.POST or None)

    if regist_form.is_valid():
        try:
            # フォームからデータを取得し、新しい Users インスタンスを作成
            user = regist_form.save(commit=False)

            # フォームで追加したフィールドに値を設定
            user.height = regist_form.cleaned_data['height']
            user.weight = regist_form.cleaned_data['weight']
            user.goal = regist_form.cleaned_data['goal']

            # パスワードの保存
            user.set_password(regist_form.cleaned_data['password'])

            # ユーザーを保存
            user.save()

            return redirect('accounts:home')

        except ValidationError as e:
            regist_form.add_error('password', e)

    return render(
        request, 'accounts/regist.html', context={
            'regist_form': regist_form,
        }
    )

def activate_user(request, token):
    UserActivateTokens.objects.activate_user_by_token(token)
    return render(
        request, 'accounts/activate_user.html'
    )
