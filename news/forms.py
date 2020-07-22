from django import forms


class CreateNewsForm(forms.Form):

    title = forms.CharField()
    content = forms.CharField()
