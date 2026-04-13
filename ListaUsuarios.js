const DivFiltroCargo = document.getElementById('DivFiltroCargo');
const FiltroCargo = document.getElementById('filtro-cargo');
const FiltroTipo = document.getElementById('filtro-tipo');
const OrdenarPor = document.getElementById('ordenar-por');
const BusquedaInput = document.getElementById('buscador');
const usuario = JSON.parse(sessionStorage.getItem('usuario'));

const ListaUsuarios = [ 
    { nombre: 'Pepito', apellido: 'Pérez', correo: 'pepito.perez@example.com', telefono: 987654321, tipo: 'estudiante_pre', cargo: '' },
    { nombre: 'Pepita', apellido: 'Pereira', correo: 'pepita.pereira@example.com', telefono: 911112222, tipo: 'estudiante_post', cargo: '' },
    { nombre: 'Juanin', apellido: 'Juanjarri', correo: 'estudiante.juanin.juanjarri@example.com', telefono: 933334444, tipo: 'funcionario', cargo: 'administrativo' },
    { nombre: 'Marcos', apellido: 'Toro', correo: 'Toro.Marcos@example.com', telefono: 922223333, tipo: 'funcionario', cargo: 'profesional' },
    { nombre: 'Carla', apellido: 'Labarca', correo: 'Profesional.Carla@example.com', telefono: 944445555, tipo: 'estudiante_post', cargo: '' },
    { nombre: 'Sofía', apellido: 'García', correo: 'sofia.garcia@example.com', telefono: 955556666, tipo: 'academico', cargo: '' },
    { nombre: 'Diego', apellido: 'Martínez', correo: 'diego.martinez@example.com', telefono: 966667777, tipo: 'funcionario', cargo: 'profesional' },
    { nombre: 'Alberto', apellido: 'Pardo', correo: 'pAlberto@example.com', telefono: 912345678, tipo: 'estudiante_pre', cargo: ''},
    { nombre: 'Fernanda', apellido: 'Vasquez', correo: 'fernanda.v@example.com', telefono: 945671234, tipo: 'funcionario', cargo: 'auxiliar'},
    { nombre: 'Agustín', apellido: 'Zuñiga', correo: 'zuñiga.a@example.com', telefono: 988887777, tipo: 'funcionario', cargo: 'coordinador'}
];

if (usuario) {
    ListaUsuarios.push(usuario);
}

FiltroTipo.addEventListener('change', () => {
    if (FiltroTipo.value == 'funcionario') {
        DivFiltroCargo.classList.add('visible');
    } else {
        DivFiltroCargo.classList.remove('visible');
        FiltroCargo.value = '';
    }
});

const por_pagina = 4;
let pagina_actual = 1;

const obtenerUsuariosFiltrados = () => {
    const tipo = FiltroTipo.value;
    const cargo = FiltroCargo.value;
    const orden = OrdenarPor.value;
    const busqueda = BusquedaInput.value.trim().toLowerCase();
    let usuarios = [...ListaUsuarios];

    if (busqueda) {
        usuarios = usuarios.filter(usuario => {
            const nombreCompleto = `${usuario.nombre} ${usuario.apellido}`.toLowerCase();
            return nombreCompleto.includes(busqueda) || usuario.correo.toLowerCase().includes(busqueda);
        });
    }

    if (tipo) {
        usuarios = usuarios.filter(u => u.tipo == tipo);
    }

    if(cargo){
        usuarios = usuarios.filter(u => u.cargo == cargo);
    }

    usuarios.sort((a,b) => a[orden].localeCompare(b[orden]))

    return usuarios;
}

const mostrarListaMiembros = () => {
    const usuarios= obtenerUsuariosFiltrados();
    const lista = document.getElementById('lista-usuarios');
    const totalPaginas = Math.ceil(usuarios.length/ por_pagina);
    const inicio = (pagina_actual - 1)*por_pagina;
    const final = inicio + por_pagina;
    const usuariosPagina = usuarios.slice(inicio,final);

    lista.innerHTML = '';
    if (usuariosPagina.length === 0) {
        lista.innerHTML = '<p>No se encontraron miembros con los parámetros ingresados.</p>';
    } else {
        usuariosPagina.forEach(u => {
            const div = document.createElement('div');
            div.classList.add('bloqueUsuario');
            div.innerHTML = `
                <p> <strong> ${u.nombre} ${u.apellido} </strong> </p>
                <p>Tipo: ${u.tipo}</p>
                <p>Correo: ${u.correo}</p>
                <p>Teléfono: +56 ${u.telefono}</p>
                ${u.cargo ? `<p>Cargo: ${u.cargo}</p>` : ''}
            `;
            lista.appendChild(div);
        });
    }

    document.getElementById('pagina-actual').textContent = `Página ${pagina_actual} de ${totalPaginas || 1}`;
    document.getElementById('boton-anterior').disabled = pagina_actual == 1;
    document.getElementById('boton-siguiente').disabled = pagina_actual >= totalPaginas;
}

BusquedaInput.addEventListener('input', () =>{
pagina_actual = 1;
mostrarListaMiembros();
});

FiltroTipo.addEventListener('input',() =>{
pagina_actual = 1;
mostrarListaMiembros();
});

FiltroCargo.addEventListener('input',() =>{
pagina_actual = 1;
mostrarListaMiembros();
});

OrdenarPor.addEventListener('input',() =>{
pagina_actual = 1;
mostrarListaMiembros();
});

document.getElementById('boton-anterior').addEventListener('click', () =>{
pagina_actual --;
mostrarListaMiembros();
})

document.getElementById('boton-siguiente').addEventListener('click', () =>{
pagina_actual ++;
mostrarListaMiembros();
})

mostrarListaMiembros();