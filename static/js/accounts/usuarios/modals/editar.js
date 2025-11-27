document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById('form-edit-user');
    const modal = document.getElementById('modal-editar-usuario');

    if (!form || !modal) return;

    const { open, close } = window.__modals;

    // ---------- BOTONES CERRAR ----------
    modal.querySelectorAll('[data-close="modal-edit"]').forEach(btn => {
        btn.addEventListener('click', () => close(modal));
    });

    function convertirFecha(fechaTexto) {
        const meses = {
            enero: '01', febrero: '02', marzo: '03', abril: '04',
            mayo: '05', junio: '06', julio: '07', agosto: '08',
            septiembre: '09', octubre: '10', noviembre: '11', diciembre: '12'
        };

        const [dia, , mesTexto, , anio] = fechaTexto.split(" ");
        const mes = meses[mesTexto.toLowerCase()];
        return `${anio}-${mes}-${dia.padStart(2, '0')}`;
    }

    // ---------- BOTONES EDITAR ----------
    // ---------- BOTONES EDITAR (versión con logs y robusta) ----------
    document.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', () => {

            const id = btn.getAttribute('data-id');
            const row = document.querySelector(`tr[data-id="${id}"]`);
            if (!row) {
                console.warn('No se encontró row para id', id);
                return;
            }

            form.setAttribute('action', `/accounts/usuarios/${id}/editar/`);
            console.log('Editando id', id);

            // ---------- CAMPOS GENERALES ----------
            const camposGenerales = [
                { name: 'username', attr: 'username' },
                { name: 'nombres', attr: 'nombres' },
                { name: 'apellido_paterno', attr: 'apellido_paterno' },
                { name: 'apellido_materno', attr: 'apellido_materno' },
                { name: 'correo', attr: 'email' },
                { name: 'fecha_nacimiento', attr: 'nacimiento' },
                { name: 'sexo', attr: 'sexo' },
                { name: 'ci', attr: 'ci' },
                { name: 'complemento_ci', attr: 'complemento' },
                { name: 'expedido', attr: 'expedido' },
                { name: 'telefono', attr: 'telefono' },
                { name: 'celular', attr: 'celular' },
                { name: 'direccion', attr: 'direccion' }
            ];

            camposGenerales.forEach(c => {
                const el = form.querySelector(`[name="${c.name}"]`);
                if (!el) return;

                let valor = row.dataset[c.attr] || "";

                if (c.name === "fecha_nacimiento" && valor) {
                    if (!/^\d{4}-\d{2}-\d{2}$/.test(valor)) {
                        try {
                            valor = convertirFecha(valor);
                        } catch (e) {
                            console.warn('Error convirtiendo fecha:', valor, e);
                            valor = ""; // no asignar valores inválidos
                        }
                    }
                }

                el.value = valor;
            });

            // ---------- ROL ----------
            const rol = (row.dataset.rol || "")
                .trim()
                .toLowerCase()
                .normalize("NFD")
                .replace(/[\u0300-\u036f]/g, "");
            console.log("ROL NORMALIZADO →", JSON.stringify(rol));
            const tipoInput = form.querySelector('[name="tipo"]');
            if (tipoInput) tipoInput.value = rol;

            // ---------- OCULTAR TODOS LOS BLOQUES ----------
            const bloques = ['edit-campos-medico','edit-campos-admision','campos-encargado-admision'];
            bloques.forEach(id => {
                const b = document.getElementById(id);
                if (b) {
                    b.style.display = 'none';
                } else {
                    console.warn('Bloque no encontrado:', id);
                }
            });

            // limpiar checkboxes del propio formulario
            form.querySelectorAll('input[type="checkbox"]').forEach(ch => ch.checked = false);

            // ---------- BLOQUE MÉDICO ----------
            if (rol === 'medico') {
                console.log('Entrando en rama MEDICO');
                const box = document.getElementById('edit-campos-medico');
                if (!box) { console.error('edit-campos-medico no existe'); }
                else {
                    box.style.display = 'block';

                    const especialidad = box.querySelector('[name="especialidad"]');
                    const matricula = box.querySelector('[name="matricula"]');
                    const consultorio = box.querySelector('[name="consultorio"]');

                    if (especialidad) {
                        const val = row.dataset.especialidadid || "";
                        especialidad.value = val;
                        console.log('especialidad set =>', val);
                    }
                    if (matricula) {
                        matricula.value = row.dataset.matricula || "";
                    }
                    if (consultorio) {
                        consultorio.value = row.dataset.consultorio || "";
                    }

                    ['madrugue','mannana','tarde','noche'].forEach(turno => {
                        const datasetKey = `medico${turno.charAt(0).toUpperCase() + turno.slice(1)}`;
                        const check = box.querySelector(`[name="med-${turno}"]`);

                        if (check) {
                            check.checked = row.dataset[datasetKey] === '1';
                        } else {
                            console.debug('checkbox medico no encontrado:', `med-${turno}`);
                        }
                    });

                    ['lunes','martes','miercoles','jueves','viernes'].forEach(dia => {
                        const check = box.querySelector(`[name="${dia}"]`);
                        if (check) {
                            check.checked = row.dataset[dia] === '1';
                        }
                    });
                    console.log(row.dataset);

                    // diagnóstico visual: comprobar estilo computado
                    const cs = window.getComputedStyle(box);
                    console.log('campos-medico computed display:', cs.display);
                }
            }

            // ---------- BLOQUE ADMISIÓN ----------
            else if (rol === 'admision') {
                console.log('Entrando en rama ADMISION');
                const box = document.getElementById('edit-campos-admision');
                if (!box) { console.error('campos-admision no existe'); }
                else {
                    box.style.display = 'block';
                    const vent = box.querySelector('[name="ventanilla"]');
                    if (vent) {
                        vent.value = row.dataset.ventanilla || "";
                    } else {
                        console.warn('input ventanilla no encontrado en admision');
                    }

                    ['madrugue','mannana','tarde','noche'].forEach(turno => {
                        const check = box.querySelector(`[name="adm-${turno}"]`);
                        if (check) {
                            check.checked = row.dataset[`adm${turno.charAt(0).toUpperCase() + turno.slice(1)}`] === '1';
                        } else {
                            console.debug('checkbox adm no encontrado:', `adm-${turno}`);
                        }
                    });
                    console.log(row.dataset);

                    console.log('campos-admision computed display:', window.getComputedStyle(box).display);
                }
            }

            // ---------- BLOQUE ENCARGADO ADMISION ----------
            else if (rol.toLowerCase() === 'encargado de admisión' 
                || rol.toLowerCase() === 'encargado de admision') {

                console.log('Entrando en rama ENCARGADO DE ADMISION');

                const box = document.getElementById('campos-encargado-admision');
                if (!box) {
                    console.error('campos-encargado-admision no existe');
                    return;
                }

                box.style.display = 'block';

                // ----------- VENTANILLA -----------
                const vent = box.querySelector('[name="enc-ventanilla"]');
                if (vent) {
                    vent.value = row.dataset.ventanillaenc || "";
                }

                // ----------- TURNOS -----------
                const claves = {
                    madrugue: "encMadrugue",
                    mannana: "encMannana",
                    tarde: "encTarde",
                    noche: "encNoche"
                };

                Object.entries(claves).forEach(([turno, datasetKey]) => {
                    const check = box.querySelector(`[name="enc-${turno}"]`);
                    if (check) {
                        check.checked = row.dataset[datasetKey] === '1';
                    }
                });
                console.log(row.dataset);

                console.log('campos-encargado-admision OK');

            } else {
                console.log('Rol no reconocido:', rol);
            }

            // ---------- ABRIR MODAL ----------
            open(modal);

            ['edit-campos-medico','edit-campos-admision','campos-encargado-admision'].forEach(id => {
                const el = document.getElementById(id);
                console.log(
                    id,
                    'inline:', el?.style.display,
                    'computed:', window.getComputedStyle(el).display
                );
            });
        });
    });


});
