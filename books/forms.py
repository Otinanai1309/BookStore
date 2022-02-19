from django import forms
from books.models import Review


class ReviewForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class':"border rounded p-2 w-full text-gray-600",
                                                        'placeholder': "Enter your review here ..."} ))
    image = forms.ImageField(required=False)
    
    class Meta:
        model = Review
        fields = ['body', 'image']
        
        # Or we can define widgets here like that
        """widgets = {'body': forms.Textarea(attrs={'class':"border rounded p-2 w-full text-gray-600",
                                                        'placeholder': "Enter your review here ..."}),
                      'image': forms.ImageField(required=False)
                     }"""
    
    