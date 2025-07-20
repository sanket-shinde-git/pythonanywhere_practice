from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm # {"form": UserCreationForm}
    success_url = reverse_lazy("login")
    template_name = "registration/sign_up.html"   