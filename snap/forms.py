from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Post

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields=('username','email','password1','password2',)


class CreatePostForm(forms.ModelForm):
    class Meta:
        fields = ('author', 'photo', 'caption', )
        model = Post

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'author'
            'photo',
            'caption',
            Submit('post', 'Post', css_class='btn primary')
        )


