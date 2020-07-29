from django import forms


class EmailForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(
        max_length=1000, required=False, widget=forms.Textarea)
