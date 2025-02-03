// Get the chart data from the data attribute
function initializeWasteChart(chartData) {
    const ctx = document.getElementById('wasteChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Waste by Category (kg)',
                data: chartData.values,
                backgroundColor: [
                    '#4CAF50',  // Green
                    '#81C784',  // Light green
                    '#C8E6C9',  // Very light green
                    '#2E7D32'   // Dark green
                ],
                borderColor: [
                    '#388E3C',
                    '#66BB6A',
                    '#A5D6A7',
                    '#1B5E20'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Waste Distribution by Category',
                    color: '#2E7D32',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Weight (kg)',
                        color: '#2E7D32'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Waste Categories',
                        color: '#2E7D32'
                    }
                }
            }
        }
    });
}