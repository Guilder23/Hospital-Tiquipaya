# Deploy en PythonAnywhere

## 1) Crear app web
1. En PythonAnywhere, crea una **Web app** manual con **Python 3.x**.
2. En la consola Bash de PythonAnywhere:
   ```bash
   cd ~
   git clone <TU_REPO_GIT> Hospital-Tiquipaya-Oficial
   cd Hospital-Tiquipaya-Oficial
   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## 2) Variables de entorno (recomendado)
Configura variables en el archivo WSGI de PythonAnywhere o desde consola con `os.environ`:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=tuusuario.pythonanywhere.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://tuusuario.pythonanywhere.com`

Puedes usar `.env.example` como referencia.

## 3) Migraciones y estáticos
En consola Bash (con venv activo):
```bash
cd ~/Hospital-Tiquipaya-Oficial
python manage.py migrate
python manage.py collectstatic --noinput
```

## 4) Configurar WSGI en PythonAnywhere
1. Abre el archivo WSGI de la web app en PythonAnywhere.
2. Reemplaza su contenido con el de `pythonanywhere_wsgi.py`.
3. Cambia `TU_USUARIO` por tu usuario real.
4. Pulsa **Reload** en la sección Web.

## 5) Configuración de archivos estáticos en panel Web
Agrega mapeo:
- URL: `/static/`
- Directory: `/home/tuusuario/Hospital-Tiquipaya-Oficial/staticfiles`

## 6) Superusuario (opcional)
```bash
python manage.py createsuperuser
```

## 7) Comandos útiles de actualización
```bash
cd ~/Hospital-Tiquipaya-Oficial
source .venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```
Luego, **Reload** en PythonAnywhere.
