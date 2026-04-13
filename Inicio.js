const usuario = JSON.parse(sessionStorage.getItem('usuario'));
const bienvenida = document.getElementById('bienvenida');
const mensajeBienvenida = document.getElementById('mensaje-bienvenida');
const mensajeRegistro = document.getElementById('mensaje-registro');

if (usuario) {
    bienvenida.textContent = `Bienvenido, ${usuario.nombre}!`;
    mensajeBienvenida.textContent = `En esta página puedes publicar tus actividades, revisar las actividades publicadas y revisar las métricas de la plataforma.`;
    mensajeRegistro.classList.remove('visible');
} else {
    bienvenida.textContent = 'Bienvenido a Actividades DCC!';
    mensajeBienvenida.textContent = 'En esta página puedes publicar tus actividades, revisar las actividades publicadas y revisar las métricas de la plataforma.';
    mensajeRegistro.classList.add('visible');
    mensajeRegistro.textContent = 'Para poder publicar actividades es necesario registrarse primero.';
}

