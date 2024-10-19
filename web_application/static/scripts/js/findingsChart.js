// findingsChart.js

document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('findingsPieChart').getContext('2d');

    const findingsPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: window.findingsLabels,
            datasets: [{
                label: 'Findings',
                data: window.findingsData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Findings Overview'
                }
            }
        }
    });
});
