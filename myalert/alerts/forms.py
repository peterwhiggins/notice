from django import forms
from django.core.exceptions import ValidationError
from .models import submittal
from django.core import validators
from datetime import date, datetime, time
import django.forms.utils
import django.forms.widgets

class DateInput(forms.DateInput):
    input_type = 'date'


class SubmitForm(forms.ModelForm):
    URGENCY = (
        ('normal', 'normal'),
        ('immediate', 'immediate'))

    SPECTROSCOPY = (
        ('low <= 1000', 'low <= 1000'),
        ('medium <= 5000', 'medium <= 5000'),
        ('high > 5000', 'high > 5000'))

    PRIORITY = (
        ('none', 'none'),
        ('urgent', 'urgent'))

    STATUS = (
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('conditional', 'conditional'),
        ('rejected', 'rejected'))

    PHOTOMETRY = (
        ('Visual', 'Visual'),
        ('CCD/CMOS', 'CCD/CMOS'),
        ('DSLR', 'DSLR'),
        ('PEP', 'PEP'))

    TS = forms.BooleanField(required=False)
    HR = forms.BooleanField(required=False)
    NI = forms.BooleanField(required=False)
    WK = forms.BooleanField(required=False)
    MO = forms.BooleanField(required=False)
    CT = forms.BooleanField(required=False)
    EB = forms.BooleanField(required=False)
    XP = forms.BooleanField(required=False)
    HE = forms.BooleanField(required=False)
    LV = forms.BooleanField(required=False)
    SP = forms.BooleanField(required=False)
    SO = forms.BooleanField(required=False)
    Vp = forms.BooleanField(required=False)
    Cp = forms.BooleanField(required=False)
    Dp = forms.BooleanField(required=False)
    Pp = forms.BooleanField(required=False)
    U = forms.BooleanField(required=False)
    B = forms.BooleanField(required=False)
    V = forms.BooleanField(required=False)
    R = forms.BooleanField(required=False)
    I = forms.BooleanField(required=False)
    uu = forms.BooleanField(required=False)
    g = forms.BooleanField(required=False)
    rr = forms.BooleanField(required=False)
    l = forms.BooleanField(required=False)
    z = forms.BooleanField(required=False)
    cv = forms.BooleanField(required=False)
    cr = forms.BooleanField(required=False)


    submitted = forms.DateField(widget=DateInput(), required=False)
    startdate = forms.DateField(widget=DateInput(), required=False)
    enddate = forms.DateField(widget=DateInput(),required=False)
    urgency = forms.ChoiceField(choices=URGENCY, widget=forms.RadioSelect, required=False)
    status = forms.ChoiceField(choices=STATUS, widget=forms.RadioSelect, required=False)
    spectroscopy = forms.ChoiceField(choices=SPECTROSCOPY, widget=forms.RadioSelect, required=False)
    photometry = forms.ChoiceField(choices=PHOTOMETRY, widget=forms.RadioSelect, required=False)
    priority = forms.ChoiceField(choices=PRIORITY, widget=forms.RadioSelect, required=False)
    justification = forms.CharField(widget=forms.Textarea(attrs={'cols': 150, 'rows': 12}), required=False)
    instructions = forms.CharField(widget=forms.Textarea(attrs={'cols': 150, 'rows': 12}), required=False)
    notes = forms.CharField(widget=forms.Textarea(attrs={'cols': 150, 'rows': 12}), required=False)
    feedback = forms.CharField(widget=forms.Textarea(attrs={'cols': 75, 'rows': 6}), required=False)
    forums = forms.CharField(widget=forms.Textarea(attrs={'cols': 75, 'rows': 6}), required=False)
    table = forms.FileField(required=False)
    #table = forms.FileField(required=False,widget=forms.FileField())


    class Meta:
        model = submittal

        fields = ['submitted','urgency','title','annum','lname','fname','affiliation','contact','approved','status','startdate','enddate','justification',
                  'instructions','notes','feedback','forums','table','TS','HR','NI','WK','MO','spectroscopy','wavelengths','Vp', 'Cp', 'Dp', 'Pp','CT','EB','XP','HE','LV','SP','SO',
                   'U','B','V','R','I','uu','g','rr','l','z','cv','cr','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12',
                  's13','s14','s15','s16','s17','s18','s19','s20','s21','s22','s23','s24','s25']


class EditForm(forms.ModelForm):

    STATUS = (
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('conditional', 'conditional'),
        ('rejected', 'rejected'))
    
    SPECTROSCOPY = (
        ('low <= 1000', 'low <= 1000'),
        ('medium <= 5000', 'medium <= 5000'),
        ('high > 5000', 'high > 5000'))

    PRIORITY = (
        ('none', 'none'),
        ('urgent', 'urgent'))

    URGENCY = (
        ('normal', 'normal'),
        ('immediate', 'immediate'))

    PHOTOMETRY = (
        ('Visual', 'Visual'),
        ('CCD/CMOS', 'CCD/CMOS'),
        ('DSLR', 'DSLR'),
        ('PEP', 'PEP'))

  
    
    TS = forms.BooleanField(required=False)
    HR = forms.BooleanField(required=False)
    NI = forms.BooleanField(required=False)
    WK = forms.BooleanField(required=False)
    MO = forms.BooleanField(required=False)
    CT = forms.BooleanField(required=False)
    EB = forms.BooleanField(required=False)
    XP = forms.BooleanField(required=False)
    HE = forms.BooleanField(required=False)
    LV = forms.BooleanField(required=False)
    SP = forms.BooleanField(required=False)
    SO = forms.BooleanField(required=False)
    Vp = forms.BooleanField(required=False)
    Cp = forms.BooleanField(required=False)
    Dp = forms.BooleanField(required=False)
    Pp = forms.BooleanField(required=False)
    U = forms.BooleanField(required=False)
    B = forms.BooleanField(required=False)
    V = forms.BooleanField(required=False)
    R = forms.BooleanField(required=False)
    I = forms.BooleanField(required=False)
    uu = forms.BooleanField(required=False)
    g = forms.BooleanField(required=False)
    rr = forms.BooleanField(required=False)
    l = forms.BooleanField(required=False)
    z = forms.BooleanField(required=False)
    cv = forms.BooleanField(required=False)
    cr = forms.BooleanField(required=False)

    submitted = forms.DateField(widget=DateInput())
    startdate = forms.DateField(widget=DateInput())
    enddate = forms.DateField(widget=DateInput())
    approved = forms.DateField(widget=DateInput(), required=False)
    status = forms.ChoiceField(choices=STATUS, widget=forms.RadioSelect, required=False)
    urgency = forms.ChoiceField(choices=URGENCY, widget=forms.RadioSelect, required=False)
    spectroscopy = forms.ChoiceField(choices=SPECTROSCOPY, widget=forms.RadioSelect, required=False)
    photometry = forms.ChoiceField(choices=PHOTOMETRY, widget=forms.RadioSelect, required=False)
    priority = forms.ChoiceField(choices=PRIORITY, widget=forms.RadioSelect, required=False)
    justification = forms.CharField(widget=forms.Textarea(attrs={'cols': 150, 'rows': 12}), required=False)
    instructions = forms.CharField(widget=forms.Textarea(attrs={'cols': 150, 'rows': 12}), required=False)
    notes = forms.CharField(widget=forms.Textarea(attrs={'cols': 150, 'rows': 12}), required=False)
    feedback = forms.CharField(widget=forms.Textarea(attrs={'cols': 75, 'rows': 6}), required=False)
    forums = forms.CharField(widget=forms.Textarea(attrs={'cols': 75, 'rows': 6}), required=False)
    table = forms.FileField(required=False)


    class Meta:
        model = submittal

        fields = ['submitted','urgency','title','annum','lname','fname','affiliation','contact','approved','status','startdate','enddate','justification',
                  'instructions','notes','feedback','forums','table','TS','HR','NI','WK','MO','spectroscopy','wavelengths','Vp', 'Cp', 'Dp', 'Pp','CT','EB','XP','HE','LV','SP','SO',
                   'U','B','V','R','I','uu','g','rr','l','z','cv','cr','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12',
                  's13','s14','s15','s16','s17','s18','s19','s20','s21','s22','s23','s24','s25']
        widgets = {
            'submitted': DateInput(),

        }

class UploadForm(forms.Form):
    firstname = forms.CharField(label="Enter first name",max_length=50)
    lastname  = forms.CharField(label="Enter last name", max_length = 10)
    email     = forms.EmailField(label="Enter Email")
    graphic   = forms.FileField(required=False) # for creating file input
