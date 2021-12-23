
from django.test import TestCase

from catalog.forms import SearchForm, HomeSearchForm, NavSearchForm


class SearchFormTest(TestCase):

    def test_search_field_in_fields(self):
        form = SearchForm()
        self.assertTrue(form.fields['search'])

    def test_search_field_is_not_required(self):
        form = SearchForm()
        self.assertFalse(form.fields['search'].required)


class HomeSearchFormTest(TestCase):

    def test_search_field_in_fields(self):
        form = HomeSearchForm()
        self.assertTrue(form.fields['search'])

    def test_search_field_is_not_required(self):
        form = HomeSearchForm()
        self.assertFalse(form.fields['search'].required)

    def test_search_field_widget(self):
        form = HomeSearchForm()
        self.assertEqual(form.fields['search'].widget.attrs,
                         {'placeholder': 'produit ou catégorie'})


class NavSearchFormTest(TestCase):

    def test_search_field_in_fields(self):
        form = NavSearchForm()
        self.assertTrue(form.fields['search'])

    def test_search_field_is_not_required(self):
        form = NavSearchForm()
        self.assertFalse(form.fields['search'].required)

    def test_search_field_widget(self):
        form = NavSearchForm()
        self.assertEqual(form.fields['search'].widget.attrs,
                         {'placeholder': 'chercher'})
