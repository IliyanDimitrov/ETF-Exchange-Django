from django import forms 

class TickerForm(forms.Form):
    ticker = forms.CharField(label='Search', max_length=5) 