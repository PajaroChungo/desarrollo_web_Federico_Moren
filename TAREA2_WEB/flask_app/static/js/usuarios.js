const DivFiltroCargo = document.getElementById('DivFiltroCargo');
const FiltroCargo = document.getElementById('filtro-cargo');
const FiltroTipo = document.getElementById('filtro-tipo');

FiltroTipo.addEventListener('change', () => {
    if (FiltroTipo.value == 'funcionario') {
        DivFiltroCargo.classList.add('visible');
    } else {
        DivFiltroCargo.classList.remove('visible');
        FiltroCargo.value = '';
    }
});

if (FiltroTipo.value == 'funcionario') {
    DivFiltroCargo.classList.add('visible');
}