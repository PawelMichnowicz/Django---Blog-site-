from django import forms
from django.contrib.auth.models import User

from .models import Comment, Tweet

class ChoiceOrderForm(forms.Form):
    # form for choice ordering posts in list of posts
    choice = forms.ChoiceField(choices=[
        ('-date_create', 'Daty dodania: od najnowszego'),
        ('date_create', 'Daty dodania: od najstarszej'),
        ('-num_likes', 'Liczby polubień'),
        ('-num_comments', 'Liczby komentarzy'),
        ('title', 'Alfabetycznie')],
        widget=forms.Select(attrs={'onchange': 'submit();'})
        )
    choice.label = 'Sortuj według:'


class ShowTweet(forms.Form):
    # form for choice param by which top posts will be sorted
    choice = forms.ChoiceField(choices=[
        ('-num_likes', 'Najwięcej polubień'),
        ('-num_comments', 'Najczęściej komentowane'),
        ('-hits', 'Najczęściej odwiedzane'),
        ],
        widget=forms.RadioSelect(attrs={'onchange': 'submit();'}))
    choice.label = 'Pokaż'

class ShowUsers(forms.Form):
    # form for choice param by which top users will be sorted
    choice = forms.ChoiceField(choices=[
        ('-num_likes', 'Najwięcej polubień'),
        ('-num_comments', 'Najczęściej komentowane'),
        ('-hits', 'Najwięcej wyświelteń'),
    ],
    widget=forms.RadioSelect(attrs={'onchange': 'submit();'}))
    choice.label = 'Pokaż'

class NewTweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['title', 'text']


class EditTweetForm(forms.ModelForm):
    # form for editing post
    class Meta:
        model = Tweet
        fields = ['text']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['style'] = 'resize: none;'
        self.fields['text'].widget.attrs['cols'] = 100
        self.fields['text'].widget.attrs['rows'] = 3
        # set a type of window for editing post


class NewCommentForm(forms.ModelForm):
    # form for new comment
    class Meta:
        model = Comment
        fields = ['text']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['style'] = 'resize: none;'
        self.fields['text'].widget.attrs['cols'] = 100
        self.fields['text'].widget.attrs['rows'] = 3
        # set a type of window for adding comment