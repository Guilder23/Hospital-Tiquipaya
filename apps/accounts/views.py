from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from django.views import View
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

def editar_usuario(request, pk):
    user = get_object_or_404(User, pk=pk)
    perfil = getattr(user, "perfil", None)

    if request.method == "POST":

        # ==========================
        # CAMPOS GENERALES
        # ==========================
        perfil.nombres = request.POST.get("nombres")
        perfil.apellido_paterno = request.POST.get("apellido_paterno")
        perfil.apellido_materno = request.POST.get("apellido_materno") or None
        perfil.fecha_nacimiento = request.POST.get("fecha_nacimiento")
        perfil.sexo = request.POST.get("sexo")
        perfil.direccion = request.POST.get("direccion")
        perfil.ci = request.POST.get("ci")
        perfil.complemento_ci = request.POST.get("complemento_ci")
        perfil.expedido = request.POST.get("expedido") or "CB"
        perfil.telefono = request.POST.get("telefono") or None
        perfil.celular = request.POST.get("celular") or None
        perfil.correo = request.POST.get("correo") or None
        perfil.save()

        user.username = request.POST.get("username")
        user.save()

        # ==========================
        # DETECTAR ROL
        # ==========================
        tipo_rol = (perfil.tipo.nombre.lower() if perfil.tipo else "").strip()

        # ==========================
        # MÉDICO
        # ==========================
        if tipo_rol == "medico":
            medico = getattr(user, "medico", None)
            if medico:

                medico.especialidad_id = request.POST.get("especialidad") or None
                medico.nro_matricula = request.POST.get("matricula") or ""
                medico.consultorio = request.POST.get("consultorio") or ""
                medico.save()

                # Turnos médico
                t = medico.turnos
                t.madrugue = bool(request.POST.get("madrugue"))
                t.mannana = bool(request.POST.get("mannana"))
                t.tarde = bool(request.POST.get("tarde"))
                t.noche = bool(request.POST.get("noche"))
                t.save()

                # Días médico
                d = medico.dias_atencion
                d.lunes = bool(request.POST.get("lunes"))
                d.martes = bool(request.POST.get("martes"))
                d.miercoles = bool(request.POST.get("miercoles"))
                d.jueves = bool(request.POST.get("jueves"))
                d.viernes = bool(request.POST.get("viernes"))
                d.save()

        # ==========================
        # ADMISIÓN
        # ==========================
        elif tipo_rol == "admision":
            adm = getattr(user, "admision", None)
            if adm:
                adm.ventanilla = request.POST.get("ventanilla") or ""
                adm.save()

                # Turnos admisión
                t = adm.turnos
                t.madrugue = bool(request.POST.get("madrugue"))
                t.mannana = bool(request.POST.get("mannana"))
                t.tarde = bool(request.POST.get("tarde"))
                t.noche = bool(request.POST.get("noche"))
                t.save()

        # ==========================
        # ENCARGADO ADMISIÓN
        # ==========================
        elif tipo_rol == "encargado_admision":
            enc = getattr(user, "encargado_admision", None)
            if enc:
                enc.ventanilla = request.POST.get("ventanilla") or ""
                enc.save()

                # Turnos encargado
                t = enc.turnos
                t.madrugue = bool(request.POST.get("madrugue"))
                t.mannana = bool(request.POST.get("mannana"))
                t.tarde = bool(request.POST.get("tarde"))
                t.noche = bool(request.POST.get("noche"))
                t.save()

        messages.success(request, "Usuario actualizado correctamente.")
        return redirect("accounts:usuario_list")

    return render(request, "accounts/usuarios/modals/editar.html", {
        "usuario": user,
        "perfil": perfil,
        "especialidades": Especialidad.objects.all(),
        "tipos": TipoUsuario.objects.all(),
    })

class UsuarioToggleActiveView(LoginRequiredMixin, UserPassesTestMixin, View):

    def post(self, request, pk):
        usuario = get_object_or_404(User, pk=pk)

        # Alternar activo ↔ inactivo
        usuario.is_active = not usuario.is_active
        usuario.save()

        return redirect('accounts:usuario_list')

    def test_func(self):
        return self.request.user.is_staff
    
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
    template_name = "accounts/usuarios/detail.html"
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.get_object()

        # PERFIL
        perfil = getattr(user, "perfil", None)
        ctx["perfil"] = perfil

        rol = perfil.tipo.nombre.lower() if perfil and perfil.tipo else None
        ctx["rol"] = rol

        # SI ES MÉDICO
        if rol == "medico":
            medico = Medico.objects.filter(user=user).select_related(
                "especialidad", "turnos", "dias_atencion"
            ).first()
            ctx["medico"] = medico

        # SI ES ADMISIÓN
        if rol == "admision":
            adm = Admision.objects.filter(user=user).select_related("turnos").first()
            ctx["admision"] = adm

        # SI ES ENCARGADO ADMISIÓN
        if rol == "encargado_admision":
            enc = EncargadoAdmision.objects.filter(user=user).select_related("turnos").first()
            ctx["encargado_admision"] = enc

        return ctx


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

