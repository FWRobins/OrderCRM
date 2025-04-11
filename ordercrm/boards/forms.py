from django import forms
from django.forms import DateInput
from django.core.exceptions import ValidationError
# from .models import Branches
from .models import Board, Column

class DateInput(forms.DateInput):
    input_type = 'date'

class TrelloAddForm(forms.Form):
    name = forms.CharField(max_length=100)
    due_date = forms.DateField(widget=DateInput())
    # branches = forms.ModelMultipleChoiceField(queryset=Branches.objects.all().order_by("branch_id"), widget=forms.CheckboxSelectMultiple())
    branches = forms.ModelMultipleChoiceField(queryset=Column.objects.all().filter(title='To Do'), widget=forms.CheckboxSelectMultiple())