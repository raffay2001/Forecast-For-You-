from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Creating our form for user Registration 
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]