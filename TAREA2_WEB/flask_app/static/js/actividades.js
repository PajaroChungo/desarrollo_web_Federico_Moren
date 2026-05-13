let archivosCombinados = [];
validateForm = (event) => {
    event.preventDefault();
    // Se crean variables con inputs del formulario
    const title = document.getElementById('Nombre-Actividad').value.trim();
    const description = document.getElementById('Descripcion-Actividad').value.trim();
    const dia = document.getElementById('Dia-Actividad').value;
    const hora = document.getElementById('Hora-Actividad').value;
    const duracion = document.getElementById('Duracion-Actividad').value;
    const category = document.getElementById('Categoria-Actividad').value;
    const files = archivosCombinados;
    const url = document.getElementById('Url-Actividad').value.trim();

    // Se crean funciones para validar cada campo del formulario
    const validateTitle = (title) => title && title.trim().length >= 5;
    const validateDescription = (description) => description.trim().length >= 10;
    const validateDia = (dia) => dia !== '';
    const validateHora = (hora) => hora !== '';
    const validateDuracion = (duracion) => duracion && parseInt(duracion) > 0;
    const validateCategory = (category) => category !== '';
    const validateFiles = (files) => files.length > 0;
    const validateUrl = (url) => {
        const urlFormat = /^(https?:\/\/)?([\w.-]+)\.([a-z]{2,})(\/\S*)?$/i;
        return urlFormat.test(url);
    }

    let isValid = true;

    // Se buscan los mensajes de error ocultos en el HTML
    const titleError = document.getElementById('error-nombre');
    const descriptionError = document.getElementById('error-descripcion');
    const diaError = document.getElementById('error-dia');
    const horaError = document.getElementById('error-hora');
    const duracionError = document.getElementById('error-duracion');
    const categoryError = document.getElementById('error-categoria');
    const filesError = document.getElementById('error-archivos');
    const urlError = document.getElementById('error-url');

    // Se validan los inputs y se muestran mensajes de error si no cumplen condiciones correspondientes
    if (!validateTitle(title)) {
        titleError.classList.add('visible');
        isValid = false;
    } else {
        titleError.classList.remove('visible');
    }
    
    if (description){
        if (!validateDescription(description)) {
            descriptionError.classList.add('visible');
            isValid = false;
        } else {
            descriptionError.classList.remove('visible');
        }
    } else {
        descriptionError.classList.remove('visible');
    }

    if (!validateDia(dia)) {
        diaError.classList.add('visible');
        isValid = false;
    } else {
        diaError.classList.remove('visible');
    }

    if (!validateHora(hora)) {
        horaError.classList.add('visible');
        isValid = false;
    } else {
        horaError.classList.remove('visible');
    }

    if (!validateDuracion(duracion)) {
        duracionError.classList.add('visible');
        isValid = false;
    } else {
        duracionError.classList.remove('visible');
    }

    if (!validateCategory(category)) {
        categoryError.classList.add('visible');
        isValid = false;
    } else {
        categoryError.classList.remove('visible');
    }

    if (!validateFiles(files)) {
        filesError.classList.add('visible');
        isValid = false;
    } else {
        filesError.classList.remove('visible');
    }

    if (url){
        if (!validateUrl(url)) {
            urlError.classList.add('visible');
            isValid = false;
        } else {
            urlError.classList.remove('visible');
        } 
    } else {
        urlError.classList.remove('visible');
    } 

    if (isValid) {
        const MyForm = document.getElementById('form-actividad');
    const formData = new FormData(MyForm);
    
    formData.delete('files');
    archivosCombinados.forEach(file => {
        formData.append('files', file);
    });
    
    fetch(MyForm.action, {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    });
    }
}

const inputFiles = document.getElementById('files');
const refrescarFotos= function() {
    const nuevosArchivos = Array.from(inputFiles.files);
    nuevosArchivos.forEach(nuevoArchivo => {
        const existe = archivosCombinados.some(f => f.name === nuevoArchivo.name);
        if (!existe) {
            archivosCombinados.push(nuevoArchivo);
        }
    })
}

inputFiles.addEventListener('change', refrescarFotos);
const MyForm = document.getElementById('form-actividad')
MyForm.addEventListener('submit', validateForm);
