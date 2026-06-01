from django.shortcuts import render, redirect

from django.contrib.auth import login

from django.contrib.auth.decorators import login_required

from .forms import RegisterForm


# =========================
# REGISTER
# =========================
def register_view(request):

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect_based_on_role(user)
    context = {
        'form': form
    }
    return render(request, 'register.html',
        context
    )


# ROLE REDIRECTION
def redirect_based_on_role(user):
    if user.role == 'manager':
        return redirect('/reports/')
    elif user.role == 'stock':
        return redirect('/inventory/')
    elif user.role == 'sales':
        return redirect('/sales/')

# PROFILE

@login_required
def profile_view(request):
    return render(request, 'profile.html')

def home(request):
    return render(request, 'home.html')