const validateForm = (event) =>{
    event.preventDefault();

    // Se crean variables para almacenar los valores de cada campo del formulario
    const name = document.getElementById('Nombre-Usuario').value;
    const surname = document.getElementById('Apellido-Usuario').value;
    const email = document.getElementById('Correo-Usuario').value;
    const telephone = document.getElementById('Telefono-Usuario').value;
    const password = document.getElementById('Contraseña-Usuario').value;
    const confirmPassword = document.getElementById('Confirmar-Contraseña-Usuario').value;
    const region = document.getElementById('Region-Usuario').value;
    const comuna = document.getElementById('Comuna-Usuario').value
    const userType = document.getElementById('Tipo-Usuario').value;
    let position = document.getElementById('Cargo-Usuario').value;
    // Se busca el Span del cargo de usuario
    const positionSpan = document.getElementById('input-cargo');

    // Se crean funciones que validan los campos del formulario
    const validateName = (name) => {
        const onlyLetters = /^[A-Za-záéíóúÁÉÍÓÚñÑüÜ\s]+$/;
        return name && name.trim().length >= 3 && onlyLetters.test(name);
    };

    const validateGmail = (email) => {
        const gmailFormat = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return gmailFormat.test(email);
    }

    const validateTelephone = (telephone) => {
        const telephoneFormatCl = /^9\d{8}$/;
        return telephoneFormatCl.test(telephone);
    }

    const validatePassword = (password) => {
        const passwordFormat = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
        return passwordFormat.test(password);
    }

    const validateRegion = (region) => region !== '';
    const validateComuna = (comuna) => comuna !== '';
    const validateUserType = (userType) => userType !== '';
    
    let isValid = true;

    // Se buscan los mensajes de error ocultos en el HTML
    const nameError = document.getElementById('error-nombre');
    const surnameError = document.getElementById('error-apellido');
    const emailError = document.getElementById('error-correo');
    const telephoneError = document.getElementById('error-telefono');
    const passwordError = document.getElementById('error-contraseña');
    const confirmPasswordError = document.getElementById('error-confirmar-contrasena');
    const regionError = document.getElementById('error-region');
    const comunaError = document.getElementById('error-comuna');
    const userTypeError = document.getElementById('error-tipo-usuario');
    const positionError = document.getElementById('error-cargo');

    // Se validan los inputs y se muestran mensajes de error si no cumplen condiciones correspondientes
    if (!validateName(name)) {
        nameError.classList.add('visible');
        isValid = false;
    } else {
        nameError.classList.remove('visible');
    }

    if (!validateName(surname)) {
        surnameError.classList.add('visible');
        isValid = false;
    } else {
        surnameError.classList.remove('visible');      
    }

    if (!validateGmail(email)) {
        emailError.classList.add('visible');
        isValid = false;
    } else {
        emailError.classList.remove('visible');
    }

    if (!validateTelephone(telephone)) {
        telephoneError.classList.add('visible');
        isValid = false;
    } else {
        telephoneError.classList.remove('visible');                
    }

    if (!validatePassword(password)) {
        passwordError.classList.add('visible');
        isValid = false;
    } else {
        passwordError.classList.remove('visible');                
    }

    if (password !== confirmPassword) {
        confirmPasswordError.classList.add('visible');
        isValid = false;
    } else {
        confirmPasswordError.classList.remove('visible');                
    }

    if (!validateRegion(region)){
        regionError.classList.add('visible');
        isValid = false;
    } else {
        regionError.classList.remove('visible');
    }

    if (!validateComuna(comuna)){
        comunaError.classList.add('visible');
        isValid = false;
    } else {
        comunaError.classList.remove('visible');
    }

    if (!validateUserType(userType)) { 
        userTypeError.classList.add('visible');
        isValid = false;
    } else {
        userTypeError.classList.remove('visible');                
    }

    if (userType == 'funcionario' && !validateUserType(position)) {
        positionError.classList.add('visible');
        isValid = false;
        position = ''; //se resetea el valor del cargo para evitar que se envíe un valor no válido
    } else {
        positionError.classList.remove('visible');               
    }

    if (isValid) { //función para enviar el formulario si todos los campos resultaron válidos
        let MyForm = document.getElementById('form-usuario');
        MyForm.submit();
    }
}

// Función para mostrar el cargo solamente si el tipo de usuario es funcionario
const MakePositionVisible = () => {
    const userType = document.getElementById('Tipo-Usuario');
    const positionSpan = document.getElementById('input-cargo');
    const positionError = document.getElementById('error-cargo');

    if (userType.value == 'funcionario') {
        positionSpan.classList.add('visible');
    } else {
        positionSpan.classList.remove('visible');
        positionError.classList.remove('visible');
    }
}

// Función para mostrar las comunas una vez seleccionada una región
const MostrarComunas = () =>{
    const regionId = document.getElementById('Region-Usuario').value;
    const comunaForm = document.getElementById('Comuna-Usuario');

    if (!regionId) {
        comunaForm.innerHTML = '<option value="">Seleccione primero una región</option>';
        comunaForm.disabled = true;
        return;
    }

    fetch(`/comunas/${regionId}`)
        .then(response => response.json())
        .then(comunas => {
            comunaForm.innerHTML = '<option value="">Seleccione una comuna</option>';
            comunas.forEach(comuna => {
                const option = document.createElement('option');
                option.value = comuna.id;
                option.textContent = comuna.nombre;
                comunaForm.appendChild(option);
            });
            comunaForm.disabled = false; 
        });
}

const MyForm = document.getElementById('form-usuario');
MyForm.addEventListener('submit', validateForm);
document.getElementById('Tipo-Usuario').addEventListener('change', MakePositionVisible);
document.getElementById('Region-Usuario').addEventListener('change', MostrarComunas);