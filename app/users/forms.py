from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from aldrovanda.validator import validate_only_numbers, validate_only_letters, validate_only_letters_and_numbers

class UserAddUserForm(UserCreationForm):
  email = forms.EmailField(
    required=True,
    error_messages = {
      'invalid': "Debes escribir un correo valido.",
      'required': "El correo es un campo obligatorio.",
    }
  )
  first_name = forms.CharField(required=True)
  last_name = forms.CharField(required=True)
  username = forms.CharField(
    error_messages = {
      'invalid': "El usuario solo puede contener numeros y letras.",
      'required': "El usuario es un campo requerido.",
      'integrity': "Un usuario con ese nombre ya existe.",
    },
    validators=[validate_only_letters_and_numbers]
  )

  class Meta:
      model = User
      fields = ("username", "email", "password1", "password2", "first_name", "last_name" )

  def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Este correo ya se encuentra en el sistema.')
        return email
  def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).count():
          raise forms.ValidationError(u'Un usuario con ese nombre ya existe.')
        return username
  def save(self, commit=True):
      user = super(UserAddUserForm, self).save(commit=False)
      user.email = self.cleaned_data["email"]
      user.first_name = self.cleaned_data["first_name"]
      user.last_name = self.cleaned_data["last_name"]
      user.is_active = False
      if commit:
          user.save()
      return user