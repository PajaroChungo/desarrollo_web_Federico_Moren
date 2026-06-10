// Se crean funciones para validar cada campo del formulario
const validateName = (name) => name && name.trim().length >= 3 && name.trim().length <= 80;
const validateText = (text) => text.trim().length >= 5;


// Se buscan los mensajes de error ocultos en el HTML
const nameError = document.getElementById('error-nombre-comentario');
const textError = document.getElementById('error-texto-comentario');

// Se validan los inputs y se muestran mensajes de error si no cumplen condiciones correspondientes
const validateForm = (name, text) => {
    let isValid = true;
    if (!validateName(name)) {
        nameError.classList.add('visible');
        isValid = false;
    } else {
        nameError.classList.remove('visible');
    }
    
    if (!validateText(text)) { 
        textError.classList.add('visible');
        isValid = false;
    } else {
        textError.classList.remove('visible');
    }

    return isValid;
}

const actividadId = document.getElementById("actividad-id").dataset.id;

function cargarComentarios() {
    fetch(`/actividad/${actividadId}/comentarios`)
        .then(response => {
            if (!response.ok) throw new Error("Error al cargar los comentarios.");
            return response.json();
        })
        .then(data => {
            const lista = document.getElementById("lista-comentarios");
            if (data.length == 0) {
                lista.textContent = "No hay comentarios aún.";
                return;
            }
            lista.innerHTML = data.map(comentario => `
                <div class="bloqueComentario">
                <p><strong>${comentario.nombre}</strong> — ${comentario.fecha}</p>
                <p>${comentario.texto}</p>
                </div>`).join("");
        })
        .catch((error) =>{
            console.error(error);
            document.getElementById("lista-comentarios").textContent = "Error al cargar comentarios.";
        });
}

function publicarComentario(nombre, texto) {
    fetch(`/actividad/${actividadId}/comentario`, {
        method: "POST",
        headers: {"Content-Type" : "application/json"},
        credentials: "include",
        cache: "no-cache",
        body: JSON.stringify({ nombre : nombre.trim(), texto: texto.trim()})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status == "ok"){
            document.getElementById('nombre-comentario').value = "";
            document.getElementById('texto-comentario').value = "";
            nameError.classList.remove('visible');
            textError.classList.remove('visible');
            cargarComentarios();
        } else {
            if (data.data.nombre) nameError.classList.add('visible');
            if (data.data.texto) textError.classList.add('visible');
        }
    })
    .catch((error) => {
        console.error(error);
        nameError.textContent = "Error de conexión, no se pudo publicar comentario, intente de nuevo";
        nameError.classList.add('visible');
    });
}

document.getElementById("btn-agregar-comentario").addEventListener("click", () => {
    const nombre = document.getElementById('nombre-comentario').value;
    const texto = document.getElementById('texto-comentario').value;
    if (!validateForm(nombre, texto)) return;
    publicarComentario(nombre, texto)
})

cargarComentarios()