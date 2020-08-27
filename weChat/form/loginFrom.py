from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, error_messages={'required': '用户名不能为空', })
    password = forms.CharField(required=True, error_messages={'required': '密码不能为空', })
    confirmPassword = forms.CharField(required=True, error_messages={'required': '确认密码不能为空', })


class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={'required': '用户名不能为空', })
    password = forms.CharField(required=True, error_messages={'required': '密码不能为空', })
