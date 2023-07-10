from django import forms

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
class MyForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    username.widget.attrs.update({'class' : 'form-control'})
    password.widget.attrs.update({'class' : 'form-control'})

class SigninForm(forms.Form):
    mobileNumber=forms.CharField(max_length=10)
    username=forms.CharField(max_length=100)
    otp=forms.CharField()
    password=forms.CharField()
    confirmPassword=forms.CharField()
    captcha = ReCaptchaField()

    mobileNumber.widget.attrs.update({'class' : 'form-control'})
    password.widget.attrs.update({'class' : 'form-control'})
    username.widget.attrs.update({'class' : 'form-control'})
    otp.widget.attrs.update({'class' : 'form-control'})
    confirmPassword.widget.attrs.update({'class' : 'form-control'})