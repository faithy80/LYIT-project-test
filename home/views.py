from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required


def index(request):
    """
    Returns the login page or redirects to
    the dashboard, if the user is logged in
    """

    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    else:
        return redirect(reverse('account_login'))
    

@login_required
def dashboard(request):
    """
    Renders the dashboard page
    """

    return render(request, 'dashboard.html')
