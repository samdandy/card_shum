from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import Record,years,team_names,grader_names,image_test
from django import forms
from django.core.validators import MinValueValidator


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="",max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="",max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
  

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

class image_upload(forms.ModelForm):
     image = forms.ImageField(required=False)
     class Meta:
          model = image_test
          fields = ['image']

class price_edit(forms.Form):
     price_field = forms.DecimalField(max_digits=10, decimal_places=2,required=False)



class card_lookup(forms.Form):
    grades = (
         ('None','None'),
         (1,1),
         (2,2),
         (3,3),
         (4,4),
         (5,5),
         (6,6),
         (7,7),
         (8,8),
         (8,8),
         (9,9),
         (10,10)
         )
    player_name = forms.CharField(required=True,label='Player Name:', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Player'}))
    team = forms.ModelChoiceField(required=True,queryset=team_names.objects.all(), empty_label="Team",widget=forms.Select(attrs={'class': 'centered-dropdown_team'}))
    year = forms.ModelChoiceField(required=True,queryset=years.objects.all(), empty_label="Year",widget=forms.Select(attrs={'class': 'centered-dropdown_year'}))
    set_name = forms.CharField(required=True,label='Set:', max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Set'}))
    parralel_name = forms.CharField(required=False,label='Parallel Name:', max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Parallel Name'}))
    parralel = forms.IntegerField(required=False,
        label='Parallel Number',
        validators=[MinValueValidator(1)],
        widget=forms.TextInput(attrs={'min': '1','class': 'centered-dropdown_year' })
    )
    autographed = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class': 'checkmark'}),label='Autographed?')
    grader = forms.ModelChoiceField(required=False,queryset=grader_names.objects.exclude(grader_name = 'No Grader'), empty_label="None",widget=forms.Select(attrs={'class': '.centered-dropdown_grader'}))
    grade = forms.ChoiceField(required=False,choices=grades, widget=forms.Select(attrs={'class': 'centered-dropdown_grader'}))

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search')
    
# Create Add Record Form
class AddRecordForm(forms.ModelForm):
	first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}), label="")
	last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}), label="")
	email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
	phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
	address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="")
	city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"City", "class":"form-control"}), label="")
	state = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"State", "class":"form-control"}), label="")
	zipcode = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Zipcode", "class":"form-control"}), label="")

	class Meta:
		model = Record
		exclude = ("user",)