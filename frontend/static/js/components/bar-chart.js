function renderActivityBarChart(data) {
    const ctx = document.getElementById('activityBarChart').getContext('2d');

    // Destroy previous chart if exists
    if (window.activityChart) {
        window.activityChart.destroy();
    }

    window.activityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Nombre de tournées',
                data: data.values,
                backgroundColor: 'rgba(59, 130, 246, 0.7)',
                borderRadius: 6,
                barThickness: 32
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `${context.raw} tournées`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0 }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    renderActivityBarChart({
        labels: ['Jan','Fév','Mar','Avr','Mai','Juin','Juil','Août','Sep','Oct','Nov','Déc'],
        values: [42, 55, 61, 58, 73, 80, 76, 69, 85, 92, 88, 97]
    });
});
