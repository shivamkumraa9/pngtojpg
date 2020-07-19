from django import forms 


class AmountForm(forms.Form):
	amount = forms.IntegerField(min_value = 5)