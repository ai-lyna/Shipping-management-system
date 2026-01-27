function renderZonesBarChart(data) {
    const ctx = document.getElementById('zonesBarChart').getContext('2d');

    // Destroy previous chart if exists
    if (window.zonesChart) {
        window.zonesChart.destroy();
    }

    window.zonesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Nombre d incidents',
                data: data.values,
                backgroundColor: 'rgba(241, 58, 58, 0.7)',
                borderRadius: 6,
                barThickness: 18
            }]
        },
        options: {
            indexAxis: 'y', 
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.raw} incidents`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: { precision: 0 }
                },
                y: {
                    grid: { display: false }
                }
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    renderZonesBarChart({
        labels: [
            'Alger Centre',
            'Oran',
            'Constantine',
            'Blida',
            'Sétif',
            'Alger Centre',
            'Oran',
            'Constantine',
            'Blida',
            'Sétif'
        ],
        values: [32, 27, 21, 18, 14,2, 27, 21, 18, 14]
    });
});
