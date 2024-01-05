from django.core.exceptions import ValidationError


def name_length_validator(value):
    if len(value) < 2:
        raise ValidationError('Name must be at least 2 characters long')
    elif 120 < len(value):
        raise ValidationError('Name can not exceed 120 characters')


def nationality_validator(value):
    if 50 < len(value):
        raise ValidationError('Nationality can not exceed 50 characters')
