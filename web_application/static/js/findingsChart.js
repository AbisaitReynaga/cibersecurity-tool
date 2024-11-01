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
                },
                datalabels: {
                    color: '#fff',  // Set label color
                    formatter: function(value, context) {
                        // Display both label and value
                        const label = context.chart.data.labels[context.dataIndex];
                        return label + ': ' + value;
                    },
                    font: {
                        weight: 'bold',
                        size: 14
                    }
                }
            }
        },
        plugins: [ChartDataLabels] // Enable the Data Labels Plugin
    });
}

// Fetch data from the API and render the chart
document.addEventListener('DOMContentLoaded', function() {
    fetch('/overview/findings')
        .then(response => response.json())
        .then(data => {
            const { findings_labels: labels, findings_data: findingsData } = data;
            renderFindingsChart(labels, findingsData);
        })
        .catch(error => {
            console.error('Error fetching findings data:', error);
        });
});
