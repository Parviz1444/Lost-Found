from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
def signup(request):
   form = UserCreationForm(request.POST or None)
   if request.method == "POST" and form.is_valid():
       form.save()
       return redirect("login")
   return render(request, "registration/signup.html", {"form": form})
