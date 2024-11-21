from django import forms


class TrafficForm(forms.Form):
    rule = forms.CharField(widget=forms.Textarea, label='Traffic')

class SuricataRuleForm(forms.Form):
    rule = forms.CharField(widget=forms.Textarea, label='Suricata')