from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from authentication.forms import LoginForm


# Create your views here.
def login_view(request):
    html = 'login.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )
    form = LoginForm()
    return render(request, html, {'form': form})


def logout_view(request):
    if request.user:
        logout(request)
    return HttpResponseRedirect(reverse('login'))
