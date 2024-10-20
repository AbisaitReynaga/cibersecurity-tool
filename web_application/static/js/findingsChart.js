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

// Fetch data from the API and render the chart
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/findings-data')
        .then(response => response.json())
        .then(data => {
            const { labels, data: findingsData } = data;
            renderFindingsChart(labels, findingsData);
        })
        .catch(error => {
            console.error('Error fetching findings data:', error);
        });
});
