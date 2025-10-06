from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _  # ✅ Import para traducciones
import re
from datetime import datetime
from .models import Worker


def validate_cuban_id(ci: str):
    """
    Validate Cuban ID according to known rules:
    - 11 digits
    - First 6 digits: birth date (AAMMDD)
    - 7th digit: century (9=1800s, 0-5=1900s, 6-8=2000s)
    - Must be at least 18 years old
    """
    # Must be 11 digits
    if not ci.isdigit() or len(ci) != 11:
        raise ValidationError(_('ID must be a valid Cuban ID (11 digits).'))

    # Extract birth date
    birth_digits = ci[:6]
    century_digit = int(ci[6])

    year = int(birth_digits[:2])
    month = int(birth_digits[2:4])
    day = int(birth_digits[4:6])

    # Determine full year
    if century_digit == 9:
        year += 1800
    elif 0 <= century_digit <= 5:
        year += 1900
    elif 6 <= century_digit <= 8:
        year += 2000
    else:
        raise ValidationError(_('The 7th digit of the ID does not correspond to a valid century.'))

    # Validate birth date
    try:
        birth_date = datetime(year, month, day)
    except ValueError:
        raise ValidationError(_('The birth date in the ID is not valid.'))

    # Check age >= 18
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 18:
        raise ValidationError(_('The worker must be at least 18 years old.'))

    return ci


class WorkerAdminForm(ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'
        labels = {
            'id': _('Worker ID'),
            'name': _('Full Name'),
            'salary': _('Salary'),
            'phone': _('Phone Number'),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise ValidationError(_('Phone number must contain only numbers.'))
        return phone

    def clean_name(self):
        name = self.cleaned_data['name']
        if re.search(r'\d', name):
            raise ValidationError(_('Name cannot contain numbers.'))
        if name:
            name = name[0].upper() + name[1:]
        return name

    def clean_salary(self):
        salary = self.cleaned_data['salary']
        if salary <= 0:
            raise ValidationError(_('Salary must be greater than 0.'))
        return salary

    def clean_id(self):
        worker_id = self.cleaned_data['id']
        return validate_cuban_id(worker_id)


class WorkerUpdateForm(ModelForm):
    class Meta:
        model = Worker
        fields = ['name', 'salary', 'phone']
        labels = {
            'name': _('Full Name'),
            'salary': _('Salary'),
            'phone': _('Phone Number'),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise ValidationError(_('Phone number must contain only numbers.'))
        return phone

    def clean_name(self):
        name = self.cleaned_data['name']
        if re.search(r'\d', name):
            raise ValidationError(_('Name cannot contain numbers.'))
        if name:
            name = name[0].upper() + name[1:]
        return name

    def clean_salary(self):
        salary = self.cleaned_data['salary']
        if salary <= 0:
            raise ValidationError(_('Salary must be greater than 0.'))
        return salary
