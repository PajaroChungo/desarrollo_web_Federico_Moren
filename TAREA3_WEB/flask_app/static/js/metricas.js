fetch("http://127.0.0.1:5000/get-stats-registersPerDay")
    .then((response) => response.json())
    .then((data) => {
    Highcharts.chart('container_1', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Cantidad de Miembros Registrados por Día'
            },
            xAxis: {
                categories: data.dias,
                title: {
                    text: 'Días'
                }
            },
            yAxis: {
                title: {
                    text: 'Cantidad de Miembros Registrados'
                }
            },
            series: [{
                name: 'Registros por Día',
                data: data.cantidad
            }]
        });
    })
    .catch((error) => console.error("Error:", error));

fetch("http://127.0.0.1:5000/get-stats-activitiesPerType")
    .then((response) => response.json())
    .then((data) => {
        const chartData = data.tipos.map((tipo, index) => ({
            name: tipo,
            y: data.cantidad[index]
        }));

        Highcharts.chart('container_2', {
            chart: {
                type: 'pie'
            },
            title: {
                text: 'Total de Actividades Extraprogramáticas por Tipo'
            },
            series: [{
                name: 'Actividades',
                colorByPoint: true,
                data: chartData
            }],
            tooltip: {
                pointFormat: '<b>{point.name}: {point.y}</b>'
            }
        });
    })
    .catch((error) => console.error('Error:', error));

fetch("http://127.0.0.1:5000/get-stats-activitiesPerDistrict")
    .then((response) => response.json())
    .then((data) => {
        Highcharts.chart('container_3', {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Total de Actividades Registradas por Comuna'
            },
            xAxis: {
                categories: data.comunas,
                title: {
                    text: 'Comunas'
                }
            },
            yAxis: {
                title: {
                    text: 'Cantidad de Actividades'
                }
            },
            series: [{
                name: 'Actividades por Comuna',
                data: data.cantidad
            }]
        });
    })
    .catch((error) => console.error('Error:', error));