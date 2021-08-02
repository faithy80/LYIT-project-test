from dashboard.views import dashboard
from django.shortcuts import redirect, reverse
import dashboard.views


def index(request):
    """
    Returns the login page or redirects to
    the dashboard, if the user is logged in
    """

    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    else:
        return redirect(reverse('account_login'))
