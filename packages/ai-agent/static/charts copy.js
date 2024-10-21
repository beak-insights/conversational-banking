document.addEventListener('DOMContentLoaded', function () {
    // Dummy Data
    const categories = ['ask', 'tools'];
    const activityTypes = ['Activity 1', 'Activity 2', 'Activity 3', 'Activity 4'];
    const users = ['User 1', 'User 2', 'User 3'];

    const dummyData = {
        ask: {
            avgDuration: 12,
            durations: [10, 12, 14, 11],
            activityCounts: [10, 12, 14, 9],
            trends: [2, 3, 4, 5],
        },
        tools: {
            avgDuration: 8,
            durations: [7, 9, 8, 6],
            activityCounts: [5, 7, 8, 6],
            trends: [3, 4, 5, 6],
        },
        users: [
            { id: 'User 1', totalAsk: 40, totalTools: 30 },
            { id: 'User 2', totalAsk: 30, totalTools: 20 },
            { id: 'User 3', totalAsk: 50, totalTools: 40 }
        ]
    };

    // 1. Average Duration by Category
    new Chart(document.getElementById('avgDurationByCategory'), {
        type: 'bar',
        data: {
            labels: categories,
            datasets: [{
                label: 'Average Duration (s)',
                data: [dummyData.ask.avgDuration, dummyData.tools.avgDuration],
                backgroundColor: ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)'],
                borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            scales: { y: { beginAtZero: true } }
        }
    });

    // 2. Activity Breakdown by Category
    new Chart(document.getElementById('activityBreakdown'), {
        type: 'pie',
        data: {
            labels: categories,
            datasets: [{
                label: 'Activities',
                data: [dummyData.ask.durations.length, dummyData.tools.durations.length],
                backgroundColor: ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)'],
                borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
                borderWidth: 1
            }]
        }
    });

    // 3. Duration Distribution for Each Category
    new Chart(document.getElementById('durationDistribution'), {
        type: 'bar',
        data: {
            labels: activityTypes,
            datasets: [
                {
                    label: 'Ask',
                    data: dummyData.ask.durations,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Tools',
                    data: dummyData.tools.durations,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: { scales: { y: { beginAtZero: true } } }
    });

    // 4. Top Activities by Average Duration
    new Chart(document.getElementById('topActivities'), {
        type: 'bar',
        data: {
            labels: activityTypes,
            datasets: [{
                label: 'Average Duration (s)',
                data: dummyData.ask.durations,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: { scales: { y: { beginAtZero: true } } }
    });

    // 5. Activity Frequency by User
    new Chart(document.getElementById('activityFrequency'), {
        type: 'bar',
        data: {
            labels: users,
            datasets: [{
                label: 'Activity Count',
                data: dummyData.users.map(user => user.totalAsk),
                backgroundColor: 'rgba(255, 206, 86, 0.2)',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1
            }]
        },
        options: { scales: { y: { beginAtZero: true } } }
    });

    // 6. Cumulative Duration by User
    new Chart(document.getElementById('cumulativeDuration'), {
        type: 'bar',
        data: {
            labels: users,
            datasets: [
                {
                    label: 'Total Ask Duration',
                    data: dummyData.users.map(user => user.totalAsk),
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Total Tools Duration',
                    data: dummyData.users.map(user => user.totalTools),
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: { scales: { y: { beginAtZero: true } } }
    });

    // 7. Trends in Activity Duration Over Time
    new Chart(document.getElementById('trendsOverTime'), {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [
                {
                    label: 'Ask Duration (s)',
                    data: dummyData.ask.trends,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    fill: false
                },
                {
                    label: 'Tools Duration (s)',
                    data: dummyData.tools.trends,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    fill: false
                }
            ]
        },
        options: { scales: { y: { beginAtZero: true } } }
    });

    // 8. Success Rate of Tool Calls (dummy logic for success rate)
    const successRateData = [90, 80];  // For example, 90% success in 'ask', 80% in 'tools'
    new Chart(document.getElementById('successRate'), {
        type: 'bar',
        data: {
            labels: ['Ask Success Rate', 'Tools Success Rate'],
            datasets: [{
                label: 'Success Rate (%)',
                data: successRateData,
                backgroundColor: ['rgba(54, 162, 235, 0.2)', 'rgba(255, 99, 132, 0.2)'],
                borderColor: ['rgba(54, 162, 235, 1)', 'rgba(255, 99, 132, 1)'],
                borderWidth: 1
            }]
        },
        options: { scales: { y: { beginAtZero: true } } }
    });

    // 9. Category Duration vs. Activity Correlation
    new Chart(document.getElementById('categoryVsDuration'), {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Ask',
                    data: [{ x: 'Activity 1', y: 10 }, { x: 'Activity 2', y: 12 }],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)'
                },
                {
                    label: 'Tools',
                    data: [{ x: 'Activity 1', y: 8 }, { x: 'Activity 2', y: 9 }],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)'
                }
            ]
        },
        options: { scales: { y: { beginAtZero: true } } }
    });
});