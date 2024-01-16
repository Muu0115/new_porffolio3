# accounts/views.py

from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistForm
from django.core.exceptions import ValidationError
from .models import UserActivateTokens
from django.http import HttpResponse


class HomeView(View):
    def get(self, request):
        return render(request, 'accounts/home.html')

    # 他に必要なメソッドがあれば追加

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
