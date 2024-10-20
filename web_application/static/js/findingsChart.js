// findingsChart.js

function renderFindingsChart(findingsLabels, findingsData) {
    const ctx = document.getElementById('findingsPieChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: findingsLabels,
            datasets: [{
                data: findingsData,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
                hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
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
}

document.addEventListener('DOMContentLoaded', function() {
    // Assuming findingsLabels and findingsData are available globally from the template
    renderFindingsChart(window.findingsLabels, window.findingsData);
});
