from django import forms

class EmailForm(forms.Form):
    recipient = forms.EmailField(label='당신의 이메일')