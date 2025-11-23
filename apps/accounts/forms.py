from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Perfil, TipoUsuario

class UserCreateWithProfileForm(UserCreationForm):
    tipo = forms.ModelChoiceField(queryset=TipoUsuario.objects.all(), required=False)
    nombres = forms.CharField(max_length=100)
    apellido_paterno = forms.CharField(max_length=100)
    apellido_materno = forms.CharField(max_length=100, required=False)
    correo_electronico = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'is_active')

    def save(self, commit=True):
        user = super().save(commit=commit)
        tipo = self.cleaned_data.get('tipo')
        Perfil.objects.update_or_create(
            user=user,
            defaults={
                'tipo': tipo,
                'nombres': self.cleaned_data.get('nombres'),
                'apellido_paterno': self.cleaned_data.get('apellido_paterno'),
                'apellido_materno': self.cleaned_data.get('apellido_materno'),
                'correo_electronico': self.cleaned_data.get('correo_electronico'),
            }
        )
        return user

class UserUpdateWithProfileForm(UserChangeForm):
    password = None
    tipo = forms.ModelChoiceField(queryset=TipoUsuario.objects.all(), required=False)
    nombres = forms.CharField(max_length=100)
    apellido_paterno = forms.CharField(max_length=100)
    apellido_materno = forms.CharField(max_length=100, required=False)
    correo_electronico = forms.EmailField(required=False)

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('username', 'is_active')

    def save(self, commit=True):
        user = super().save(commit=commit)
        tipo = self.cleaned_data.get('tipo')
        Perfil.objects.update_or_create(
            user=user,
            defaults={
                'tipo': tipo,
                'nombres': self.cleaned_data.get('nombres'),
                'apellido_paterno': self.cleaned_data.get('apellido_paterno'),
                'apellido_materno': self.cleaned_data.get('apellido_materno'),
                'correo_electronico': self.cleaned_data.get('correo_electronico'),
            }
        )
        return user
