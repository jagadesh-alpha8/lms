from django.shortcuts import render
from .forms import RegistrationForm


def registration_view(request):
    """
    Single view for handling registration form - GET and POST
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "success.html")
    else:
        form = RegistrationForm()
    
    return render(request, "form.html", {"form": form})