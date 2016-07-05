from django import forms
from django.forms import ModelForm

from athletesunited.communities.models import CommunityPost

# Community Post Form
class CommunityPostForm(ModelForm):
    body = forms.CharField(label='', widget = forms.Textarea({'placeholder': 'Post a question or share something of value'}))
    
    class Meta:
        model = CommunityPost
        fields = ['body']

# Community Post Form
class CommunityPostAskAProForm(ModelForm):
    body = forms.CharField(label='', widget = forms.Textarea({'placeholder': 'Post a question or share something of value'}))
    bounty = forms.DecimalField(label='Bounty: ', required = True, initial=0.00)
    
    class Meta:
        model = CommunityPost
        fields = ['body', 'bounty']





