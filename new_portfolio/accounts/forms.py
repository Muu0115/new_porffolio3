from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Users

class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢', min_value=0, error_messages={'invalid': '半角数字で入力してください'})
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())

    height = forms.DecimalField(label='身長', required=False)
    weight = forms.DecimalField(label='体重', required=False)
    goal = forms.CharField(label='今後の目標', required=False, widget=forms.Textarea(attrs={'rows': 4}))

    class Meta():
        model = Users
        fields = ('username', 'age', 'email', 'password', 'confirm_password', 'height', 'weight', 'goal')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')

        age = str(cleaned_data['age'])
        if not age.isdigit():
            raise forms.ValidationError('半角数字で入力してください')


        age = forms.IntegerField(
        label='年齢',
        min_value=0,
        error_messages={'invalid': '半角数字で入力してください'},
    )

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
