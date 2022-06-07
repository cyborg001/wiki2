from django import forms

class MyForm(forms.Form):
    Entry = forms.CharField()

class NewPageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
