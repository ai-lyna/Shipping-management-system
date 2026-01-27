function renderTourneesLineChart(data) {
    const ctx = document.getElementById('tourneesLineChart').getContext('2d');

    // Destroy previous chart if exists
    if (window.myChart) {
        window.myChart.destroy();
    }

    window.tourneesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.months,
            datasets: [{
                label: 'Nombre de tournées',
                data: data.values,
                borderColor: 'rgb(255, 163, 42)',
                backgroundColor: 'rgba(255, 182, 80, 0.15)',
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: 'rgb(228, 170, 94)',
                pointBorderColor: '#fff',
                pointHoverRadius: 6
            }]
        },
        options: {
            interaction: {
                mode: 'nearest',
                intersect: false
            },
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.raw} tournées`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0 }
                }
            }
        }
    });
}

// Example usage
document.addEventListener("DOMContentLoaded", function() {
    renderTourneesLineChart({
        months: ['Jan','Fév','Mar','Avr','Mai','Juin','Juil','Août','Sep','Oct','Nov','Déc'],
        values: [42, 55, 61, 58, 73, 80, 76, 69, 85, 92, 88, 97]
    });
});
