from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
import re
from .models import Worker


class WorkerAdminForm(ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'
        labels = {
            'id': 'Worker ID',
            'name': 'Full Name',
            'salary': 'Salary',
            'phone': 'Phone Number',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Phone should contain only digits
            if not phone.isdigit():
                raise ValidationError("Phone number must contain only numbers.")
        return phone

    def clean_name(self):
        name = self.cleaned_data['name']
        # Name should not contain numbers
        if re.search(r'\d', name):
            raise ValidationError("Name cannot contain numbers.")
        # Capitalize first letter
        if name:
            name = name[0].upper() + name[1:]
        return name

    def clean_salary(self):
        salary = self.cleaned_data['salary']
        if salary <= 0:
            raise ValidationError('Salary must be greater than 0')
        return salary

    #falta validacion de carnet
    def clean_id(self):
        worker_id = self.cleaned_data['id']
        # Make first character uppercase
        if worker_id:
            worker_id = worker_id[0].upper() + worker_id[1:]
        # Validate Cuban carnet format: 11 digits
        if not re.fullmatch(r'\d{11}', worker_id):
            raise ValidationError("ID must be a Cuban carnet (11 digits).")
        return worker_id


class WorkerUpdateForm(ModelForm):
    class Meta:
        model = Worker
        fields = 'name', 'salary', 'phone'
        labels = {
            'id': 'Worker ID',
            'name': 'Full Name',
            'salary': 'Salary',
            'phone': 'Phone Number',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Phone should contain only digits
            if not phone.isdigit():
                raise ValidationError("Phone number must contain only numbers.")
        return phone

    def clean_name(self):
        name = self.cleaned_data['name']
        # Name should not contain numbers
        if re.search(r'\d', name):
            raise ValidationError("Name cannot contain numbers.")
        # Capitalize first letter
        if name:
            name = name[0].upper() + name[1:]
        return name

    def clean_salary(self):
        salary = self.cleaned_data['salary']
        if salary <= 0:
            raise ValidationError('Salary must be greater than 0')
        return salary

    #falta validacion de carnet
    def clean_id(self):
        worker_id = self.cleaned_data['id']
        # Make first character uppercase
        if worker_id:
            worker_id = worker_id[0].upper() + worker_id[1:]
        # Validate Cuban carnet format: 11 digits
        if not re.fullmatch(r'\d{11}', worker_id):
            raise ValidationError("ID must be a Cuban carnet (11 digits).")
        return worker_id
