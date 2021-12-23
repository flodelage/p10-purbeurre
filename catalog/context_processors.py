
from .forms import NavSearchForm


def nav_bar_form(request):
    """
    Add navbar form to all contexts
    """
    navbar_form = NavSearchForm()
    return {'navbar_form': navbar_form}
