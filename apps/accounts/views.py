from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import UserCreateWithProfileForm, UserUpdateWithProfileForm

from django.contrib import messages 
from django.contrib.auth.models import User 
from apps.accounts.models import ( Perfil, TipoUsuario, Medico, Admision, EncargadoAdmision ) 
from apps.horarios.models import DiasAtencion, HorariosAtencion
from apps.especialidades.models import Especialidad

# Registro simple
def crear_usuario(request):
    if request.method == "POST":

        # ================================
        # 1. CREAR USUARIO DJANGO
        # ================================
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return redirect("usuario_list")

        user = User.objects.create_user(
            username=username,
            password=password,
        )

        # ================================
        # 2. CREAR PERFIL
        # ================================
        tipo_rol = request.POST.get("tipo")
        tipo_obj = None

        if tipo_rol:
            tipo_obj = TipoUsuario.objects.filter(nombre__iexact=tipo_rol).first()

        perfil = Perfil.objects.create(
            user=user,
            nombres=request.POST.get("nombres"),
            apellido_paterno=request.POST.get("apellido_paterno"),
            apellido_materno=request.POST.get("apellido_materno") or None,
            fecha_nacimiento=request.POST.get("fecha_nacimiento"),
            sexo=request.POST.get("sexo"),
            direccion=request.POST.get("direccion"),
            ci=request.POST.get("ci"),
            complemento_ci=request.POST.get("complemento_ci"),
            expedido=request.POST.get("expedido") or "CB",
            telefono=request.POST.get("telefono") or None,
            celular=request.POST.get("celular") or None,
            correo=request.POST.get("correo") or None,
            tipo=tipo_obj
        )

        # ================================
        # 3. CREAR HORARIOS (TODOS LOS ROLES)
        # ================================
        if tipo_rol != "":
            turnos = HorariosAtencion.objects.create(
                madrugue=bool(request.POST.get("madrugue")),
                mannana=bool(request.POST.get("mannana")),
                tarde=bool(request.POST.get("tarde")),
                noche=bool(request.POST.get("noche")),
            )

        # ================================
        # 4. SI ES MÉDICO → CREAR DÍAS
        # ================================
        if tipo_rol == "medico":
            dias = DiasAtencion.objects.create(
                lunes=bool(request.POST.get("lunes")),
                martes=bool(request.POST.get("martes")),
                miercoles=bool(request.POST.get("miercoles")),
                jueves=bool(request.POST.get("jueves")),
                viernes=bool(request.POST.get("viernes")),
            )

            Medico.objects.create(
                user=user,
                especialidad_id=request.POST.get("especialidad") or None,
                nro_matricula=request.POST.get("nro_matricula") or "",
                consultorio=request.POST.get("consultorio") or "",
                turnos=turnos,
                dias_atencion=dias,
            )

        # ================================
        # 5. SI ES ADMISIÓN
        # ================================
        elif tipo_rol == "admision":
            Admision.objects.create(
                user=user,
                ventanilla=request.POST.get("ventanilla") or "",
                turnos=turnos
            )

        # ================================
        # 6. SI ES ENCARGADO DE ADMISIÓN
        # ================================
        elif tipo_rol == "encargado_admision":
            EncargadoAdmision.objects.create(
                user=user,
                ventanilla=request.POST.get("ventanilla") or "",
                turnos=turnos
            )

        messages.success(request, "Usuario creado correctamente.")
        return redirect("accounts:usuario_list")

    # GET
    return render(request, "accounts/usuarios/modals/crear.html", {
        "especialidades": Especialidad.objects.all(),
        "tipos": TipoUsuario.objects.all(),
    })

# Función para verificar si un usuario es administrador
def _es_admin(user):
    if user.is_superuser or user.is_staff:
        return True
    try:
        perfil = user.perfil
    except Perfil.DoesNotExist:
        return False
    if perfil.tipo is None:
        return False
    return perfil.tipo.nombre.lower() == 'administrador'

# ----- Tipos de Usuario -----
class TipoUsuarioListView(LoginRequiredMixin, ListView):
    model = TipoUsuario
    template_name = 'accounts/tipos/list.html'

class TipoUsuarioCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TipoUsuario
    fields = ['nombre','descripcion']
    template_name = 'accounts/tipos/form.html'
    success_url = reverse_lazy('accounts:tipousuario_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creado_por = self.request.user
        form.instance = obj
        return super().form_valid(form)

class TipoUsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TipoUsuario
    fields = ['nombre','descripcion']
    template_name = 'accounts/tipos/form.html'
    success_url = reverse_lazy('accounts:tipousuario_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.actualizado_por = self.request.user
        form.instance = obj
        return super().form_valid(form)

class TipoUsuarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TipoUsuario
    template_name = 'accounts/tipos/confirm_delete.html'
    success_url = reverse_lazy('accounts:tipousuario_list')

    def test_func(self):
        return self.request.user.is_staff

# ----- Usuarios -----
class UsuarioListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/usuarios/list.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        return get_user_model().objects.prefetch_related('perfil').all().order_by('username')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tipos'] = TipoUsuario.objects.all()
        ctx['puede_admin'] = _es_admin(self.request.user)
        ctx['especialidades'] = Especialidad.objects.all()
        return ctx

class UsuarioDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/usuarios/detail.html'

class UsuarioCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = UserCreateWithProfileForm
    template_name = 'accounts/usuarios/form.html'
    success_url = reverse_lazy('accounts:usuario_list')

    def test_func(self):
        return _es_admin(self.request.user)

class UsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateWithProfileForm
    template_name = 'accounts/usuarios/form.html'
    success_url = reverse_lazy('accounts:usuario_list')

    def test_func(self):
        return _es_admin(self.request.user)

class UsuarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = get_user_model()
    template_name = 'accounts/usuarios/confirm_delete.html'
    success_url = reverse_lazy('accounts:usuario_list')

    def test_func(self):
        return _es_admin(self.request.user)
