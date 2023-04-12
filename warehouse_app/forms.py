from django import forms
import datetime


class DateForms(forms.Form):
    first_date = forms.DateField(initial=datetime.date.today)
    second_date = forms.DateField(initial=datetime.date.today)
