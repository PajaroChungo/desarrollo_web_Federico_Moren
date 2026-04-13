const usuario = JSON.parse(sessionStorage.getItem('usuario'));
tituloRegistro = document.getElementById('titulo-registro');
mensajeRegistro = document.getElementById('mensaje-registro');
botonRegistro = document.getElementById('boton-registro');
MyForm = document.getElementById('form-actividad');

if (usuario) {
    tituloRegistro.classList.add('visible');
    mensajeRegistro.classList.remove('visible');
    botonRegistro.classList.remove('visible');
    MyForm.classList.add('visible');
} else {
    tituloRegistro.classList.remove('visible');
    mensajeRegistro.classList.add('visible');
    botonRegistro.classList.add('visible');
    MyForm.classList.remove('visible');
}

validateForm = (event) => {
    event.preventDefault();
    // Se crean variables con inputs del formulario
    const title = document.getElementById('Nombre-Actividad').value.trim();
    const description = document.getElementById('Descripcion-Actividad').value.trim();
    const date = document.getElementById('Fecha-Actividad').value;
    const category = document.getElementById('Categoria-Actividad').value;
    const files = document.getElementById('files').files;
    const url = document.getElementById('Url').value.trim();

    // Se crean funciones para validar cada campo del formulario
    const validateTitle = (title) => title && title.trim().length >= 5;
    const validateDescription = (description) => description && description.trim().length >= 10;
    const validateDate = (date) => date !== '';
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
    const dateError = document.getElementById('error-fecha');
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

    if (!validateDescription(description)) {
        descriptionError.classList.add('visible');
        isValid = false;
    } else {
        descriptionError.classList.remove('visible');
    }

    if (!validateDate(date)) {
        dateError.classList.add('visible');
        isValid = false;
    } else {
        dateError.classList.remove('visible');
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

    if (!validateUrl(url)) {
        urlError.classList.add('visible');
        isValid = false;
    } else {
        urlError.classList.remove('visible');
    }   

    if (isValid) {
        crearActividad(title, description, date, category, files, url);
        let MyForm = document.getElementById('form-actividad');
        MyForm.reset();
    }
}

crearActividad = (title, description, date, category, files, url) => {
    //Lista donde agregar la estructura de la actividad creada
    let ListaActividades = document.getElementById('lista-actividades');

    //Se crea la estructura de la actividad
    const actividad = document.createElement('div');
    actividad.classList.add('bloqueActividad');
    
    //Se crea los "p" donde se muestran los datos de la actividad
    const tituloSpan = document.createElement('p');
    tituloSpan.textContent = title;

    const NombreUsuario = usuario.nombre
    const ApellidoUsuario = usuario.apellido
    const autorSpan = document.createElement('p');
    autorSpan.textContent = `Actividad organizada por: ${NombreUsuario} ${ApellidoUsuario}`;

    const descripcionSpan = document.createElement('p');
    descripcionSpan.textContent = description;

    const categoriaSpan = document.createElement('p');
    categoriaSpan.textContent = `Categoría: ${category}`;

    const fechaSpan = document.createElement('p');
    fechaSpan.textContent = `Fecha: ${date}`;

    const GmailUsuario = usuario.correo;
    const TelefonoUsuario = usuario.telefono;
    const InfoContactoSpan = document.createElement('p');
    InfoContactoSpan.textContent = `Contacto: ${GmailUsuario} | +56 ${TelefonoUsuario}`;

    const urlSpan = document.createElement('a');
    urlSpan.textContent = `Más información aquí`;
    urlSpan.href = url;
    urlSpan.target = '_blank';

    //Mostrar imágenes adjuntas
    const ContenedorArchivos = document.createElement('div');
    Array.from(files).forEach(file => {
        const fileURL = URL.createObjectURL(file);
        if (file.type.startsWith('image/')) {
            const img = document.createElement('img');
            img.src = fileURL;
            img.alt = file.name;
            img.style.width = '100%';
            img.style.maxWidth = '400px';
            img.style.height = 'auto';
            img.style.objectFit = 'unset'; 
            ContenedorArchivos.appendChild(img);
        } else if (file.type.startsWith('video/')) {
            const video = document.createElement('video');
            video.src = fileURL;
            video.controls = true;
            video.style.width = '100%';
            video.style.maxWidth = '400px';
            video.style.height = '250px';
            ContenedorArchivos.appendChild(video);
        }
    });

    //Se agrega cada "p" a la estructura de la actividad
    actividad.appendChild(tituloSpan);
    actividad.appendChild(autorSpan);
    actividad.appendChild(descripcionSpan);
    actividad.appendChild(categoriaSpan);
    actividad.appendChild(fechaSpan);
    actividad.appendChild(InfoContactoSpan);
    actividad.appendChild(urlSpan);
    actividad.appendChild(ContenedorArchivos);

    //Se agrega la actividad a la lista de actividades
    ListaActividades.prepend(actividad);
}

MyForm.addEventListener('submit', validateForm);
