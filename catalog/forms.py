
from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=False
    )


class HomeSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={'placeholder': 'produit ou catégorie'} )
    )


class NavSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={'placeholder': 'chercher'})
    )
