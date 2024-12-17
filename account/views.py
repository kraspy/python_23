from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'account/login.html'


@login_required
def confirm_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return render(request, "account/confirm_logout.html")
