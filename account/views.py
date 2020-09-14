from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # Above we are creating an object of our login form and assigining it to a variable named "form"
        if form.is_valid():
            cd = form.cleaned_data
            # The line returns a dictionary of the form fields {"field":"value"} into cd
            user = authenticate(request, username=cd['username'], password=cd['password'])
            # Now we are basically making an authenticated user by authenticating it against "DB"
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # By the above method, we are setting the user in the session
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

# The below decorator checks if the current user is authenticated
# If the user if authenticated Django executes the below function
# But if the user is not authenticated then Django redirects the user to the originally passed next parameter URL
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})