from django import forms
from .models import Comment


class EmailForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(
        max_length=1000, required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'mail', 'body')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'inline_field'
        self.fields['mail'].widget.attrs['class'] = 'inline_field'
        self.fields['body'].widget.attrs['class'] = 'block_field'
