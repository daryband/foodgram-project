from django.shortcuts import redirect, render

from .forms import UserSignupForm


def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'registration/signup.html', {'form': form})
    else:
        form = UserSignupForm()
        return render(request, 'registration/signup.html', {'form': form})
