from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'Write Comment',
                'class': 'form-style-1',
                'style': 'height: 230px; background-color: #233a50; color: #ffffff; border: 3px solid #0f2133;  border-radius: 3px;',
            })
        }
        
class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }
