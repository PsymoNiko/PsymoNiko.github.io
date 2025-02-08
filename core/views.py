from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def handle_root_redirect(request):
    # Redirect to the index page
    return redirect('index')
