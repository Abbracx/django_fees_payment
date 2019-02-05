from django import forms
from djapp.models import Institute, Branch


class UserForm(forms.Form):
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(label='User Name', max_length=25, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    firstname = forms.CharField(label='First Name', max_length=25, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Firstname'}))
    lastname = forms.CharField(label='Last Name', max_length=25, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Lastname'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    mobile = forms.CharField(label='Mobile', max_length=10, required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))
    enrollment = forms.CharField(
        label='Mobile', max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enrollment Number'}))
    birth_date = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Birth Date'}), required=True)
    institute = forms.ModelChoiceField(queryset=Institute.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'id_inst'}), required=True)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'id_branch'}), required=True)
    CHOICES = (('btech', 'B Tech'), ('mba', 'MBA'),
               ('msc', 'MSC'), ('bca', 'BCA'))
    course = forms.ChoiceField(choices=CHOICES, widget=forms.Select(
        attrs={'class': 'form-control'}), required=True)
    gender = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={'class': 'form-element'}), choices=(('male', 'Male'), ('female', 'Female')))


class DocumentForm(forms.Form):
    docfile = forms.FileField()
