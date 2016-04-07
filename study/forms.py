from django import forms

class TestForm(forms.Form):
    commenter = forms.CharField(label='Enter your name', max_length = 100)
    email = forms.EmailField(label='Email (optional)')
    comment = forms.CharField(
        label = 'Type in your comments', 
        widget = forms.Textarea(
            attrs = {'class':'materialize-textarea'}
        )
    )
    uploadfile = forms.FileField(label="Upload Image")
