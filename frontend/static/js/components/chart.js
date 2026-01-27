function renderLivraisonChart(data) {
    const ctx = document.getElementById('livraisonPieChart').getContext('2d');

    // Destroy previous chart if exists
    if (window.livraisonChart) {
        window.livraisonChart.destroy();
    }

    window.livraisonChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Réussites', 'Échecs', 'En retard'],
            datasets: [{
                label: 'Livraisons',
                data: [
                    data.reussites || 0, 
                    data.echecs || 0, 
                    data.en_retard || 0
                ],
                backgroundColor: [
                    'rgb(108, 255, 120)',  
                    'rgb(255, 101, 101)',  
                    'rgb(255, 246, 83)'   
                ],
                borderColor: '#fff',
                borderWidth: 2,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                   display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label;
                            const value = context.raw;
                            const total = context.dataset.data.reduce((a,b) => a+b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Example: render chart with default data
document.addEventListener("DOMContentLoaded", function() {
    renderLivraisonChart({
        reussites: 120,
        echecs: 15,
        en_retard: 25
    });
});
