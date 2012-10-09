from django.core.exceptions import ValidationError
import re

def validate_only_numbers(value):
  if re.search("(\D+)", value):
    raise ValidationError(u'Este campo solo puede contener numeros.')

def validate_only_letters(value):
  if not re.search("([a-zA-Z]+)", value):
    raise ValidationError(u'Este campo solo puede contener letras.')

def validate_only_letters_and_numbers(value):
  if re.search("(\W+)", value):
    raise ValidationError(u'Este campo solo puede contener letras y numeros.')