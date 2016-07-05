from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from athletesunited.athletes.models import Athlete, AthleteEmail, Follow
from athletesunited.communities.models import Community, Country, City

# Athlete Registration Form
class AthleteRegistrationForm(ModelForm):
    username = forms.CharField(label='User Name:', help_text='This becomes your public URL.')
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label='Confirm Password:', widget=forms.PasswordInput(render_value=False))
    email = forms.EmailField(label='Email Address:')
    first_name = forms.CharField(label='First Name:')
    last_name = forms.CharField(label='Last Name:')

    class Meta:
        model = Athlete
        fields = ['email', 'password', 'password1', 'username', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("That athlete username is already taken, please select another.")

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError("The passwords do not match. Please try again.")
        return self.cleaned_data

# Athlete Login Form
class AthleteLoginForm(forms.Form):
    email = forms.CharField(label='Email:')
    password = forms.CharField(label='Password:',
        widget=forms.PasswordInput(render_value=False)
    )

    def clean(self):
       user = self.authenticate_via_email()
       if not user:
           raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
       else:
           self.user = user
       return self.cleaned_data

    def authenticate_user(self):
       return authenticate(
           username=self.user.username,
           password=self.cleaned_data['password'])

    def authenticate_via_email(self):
        """
        Authenticate user using email.
        Returns user object if authenticated else None
        """
        email = self.cleaned_data['email']
        if email:
           try:
               user = User.objects.get(email__iexact=email)
               if user.check_password(self.cleaned_data['password']):
                   return user
           except ObjectDoesNotExist:
               pass
        return None

# User Update Profile Form
class UserProfileUpdateForm(ModelForm):
    username = forms.CharField(label='User Name:', help_text='This becomes your public URL.')
    first_name = forms.CharField(label='First Name:')
    last_name = forms.CharField(label='Last Name:')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean_athlete_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("That athlete username is already taken, please select another.")

# Athlete Update Profile Form
class AthleteProfileUpdateForm(ModelForm):
    headline = forms.CharField(label='Headline:')
    bio = forms.CharField(label='Bio', widget = forms.Textarea())
    web_url = forms.URLField(label='Website')
    avatar = forms.ImageField(label='Profile Picture:')
    birthday = forms.CharField(label='Birthday:', help_text='Format: MM/DD/YYYY')
    communities = forms.ModelMultipleChoiceField(queryset=Community.objects.all(), label='Communities:', required=False, widget=forms.CheckboxSelectMultiple)
    countries = forms.ModelMultipleChoiceField(queryset=Country.objects.all(), label='Countries:', required=False, widget=forms.CheckboxSelectMultiple)
    cities = forms.ModelMultipleChoiceField(queryset=City.objects.all(), label='Cities:', required=False, widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Athlete
        fields = ['headline', 'bio', 'web_url', 'avatar', 'birthday', 'communities', 'countries', 'cities']

# Athlete Profile Edit Update Email Form
class AthleteProfileEditUpdateEmailForm(ModelForm):
    emails = forms.ModelChoiceField(queryset=AthleteEmail.objects.all(), label='Set a Primary Email Address:', widget=forms.RadioSelect())

    class Meta:
        model = AthleteEmail
        fields = ['emails']

# Athlete Profile Edit Add Email Form
class AthleteProfileEditAddEmailForm(ModelForm):
    email = forms.EmailField(label='Email Address:')
    
    class Meta:
        model = AthleteEmail
        fields = ['email']

# Athlete Follow Form
class FollowForm(ModelForm):
    
    class Meta:
        model = Follow
        fields = []



