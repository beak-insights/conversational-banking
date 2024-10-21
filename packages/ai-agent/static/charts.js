document.addEventListener('DOMContentLoaded', function () {
    // activitiesDataset variable is now available from FastAPI context
    // Process the activitiesDataset data to create charts
    const users = [...new Set(activitiesDataset.map(act => act.user_id))];  // Get unique users
    document.getElementById('totalUsers').innerHTML = users.length;

    const askActivities = activitiesDataset.filter(act => act.category === 'ask');
    const toolActivities = activitiesDataset.filter(act => act.category === 'tool');

    // Calculate average duration for 'ask' and 'tool'
    const avgDurationAsk = askActivities.reduce((sum, act) => sum + act.duration, 0) / askActivities.length;
    const avgDurationTools = toolActivities.reduce((sum, act) => sum + act.duration, 0) / toolActivities.length;

    // 1. Activity Breakdown by Category (Pie chart showing the number of activitiesDataset for ask/tool)
    new Chart(document.getElementById('activityBreakdown'), {
        type: 'pie',
        data: {
            labels: ['ask', 'tool'],
            datasets: [{
                label: 'Activities Count',
                data: [askActivities.length, toolActivities.length],
                backgroundColor: ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)'],
                borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Activities Count',
                    font: {
                        size: 20
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                }
            }
        }
    });


    // 2. Average Duration by Category
    new Chart(document.getElementById('avgDurationByCategory'), {
        type: 'bar',
        data: {
            labels: ['ask', 'tool'],
            datasets: [{
                label: 'Average Duration (s)',
                data: [avgDurationAsk, avgDurationTools],
                backgroundColor: ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)'],
                borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            scales: { y: { beginAtZero: true } },
            plugins: {
                title: {
                    display: true,
                    text: 'Category Average Duration',
                    font: {
                        size: 20
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                }
            }
        }
    });

    // 3. Group toolActivities by activity and calculate the average duration for each activity
    const activityDurations = toolActivities.reduce((acc, act) => {
        // If the activity doesn't exist in the accumulator, initialize it
        if (!acc[act.activity]) {
            acc[act.activity] = { totalDuration: 0, count: 0 };
        }
        // Add the duration and increment the count
        acc[act.activity].totalDuration += act.duration;
        acc[act.activity].count += 1;

        return acc;
    }, {});

    // Calculate the average duration for each activity
    const avgActivityDurations = Object.keys(activityDurations).map(activity => ({
        activity,
        avgDuration: activityDurations[activity].totalDuration / activityDurations[activity].count
    }));

    // Sort the activities by average duration in descending order
    avgActivityDurations.sort((a, b) => b.avgDuration - a.avgDuration);

    // Prepare data for the chart
    const topActivityNames = avgActivityDurations.map(act => act.activity);
    const topActivityDurations = avgActivityDurations.map(act => act.avgDuration);

    new Chart(document.getElementById('topActivities'), {
        type: 'bar',
        data: {
            labels: topActivityNames,
            datasets: [{
                label: 'Average Duration (s)',
                data: topActivityDurations,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: { 
            scales: { y: { beginAtZero: true } },
            plugins: {
                title: {
                    display: true,
                    text: 'Tools Average Duration',
                    font: {
                        size: 20
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                }
            }
        }
    });

    // 4. Trends in Activity Duration Over Time (Line chart showing duration trends over time)
    // Function to group data by day, calculate the average duration, and sort by date
    function groupAndSortByDay(data) {
        const groupedData = {};
        data.forEach(act => {
            // Get the date string in 'YYYY-MM-DD' format
            const date = new Date(act.created).toISOString().split('T')[0];

            // Initialize if not already in groupedData
            if (!groupedData[date]) {
                groupedData[date] = { totalDuration: 0, count: 0 };
            }

            // Add duration and increment count
            groupedData[date].totalDuration += act.duration;
            groupedData[date].count += 1;
        });

        // Convert groupedData to array of { x, y } format and sort by date
        return Object.keys(groupedData)
            .map(key => ({
                x: new Date(key), // Convert the date string back to a Date object
                y: groupedData[key].totalDuration / groupedData[key].count
            }))
            .sort((a, b) => a.x - b.x); // Sort by date
    }

    // Group and sort the ask and tool data by day
    const groupedAndSortedAskData = groupAndSortByDay(askActivities);
    const groupedAndSortedToolsData = groupAndSortByDay(toolActivities);

    // Create the chart with the daily aggregated and sorted data
    new Chart(document.getElementById('trendsOverTime'), {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Ask Duration (s)',
                    data: groupedAndSortedAskData,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    fill: false,
                    tension: 0.1,
                    parsing: {
                        xAxisKey: 'x',
                        yAxisKey: 'y'
                    }
                },
                {
                    label: 'Tools Duration (s)',
                    data: groupedAndSortedToolsData,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    fill: false,
                    tension: 0.1,
                    parsing: {
                        xAxisKey: 'x',
                        yAxisKey: 'y'
                    }
                }
            ]
        },
        options: { 
            scales: { 
                x: {
                    type: 'time',
                    time: {
                        unit: 'day', // Set the time unit to 'day'
                        tooltipFormat: 'yyyy-MM-dd', // Display the date in the tooltip
                    },
                    title: {
                        display: true,
                        text: 'Time (Daily)',
                        font: {
                            size: 14
                        }
                    }
                },
                y: { 
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Average Duration (s)',
                        font: {
                            size: 14
                        }
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Daily Average Duration Trends',
                    font: {
                        size: 20
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                }
            }
        }
    });

    // 5. 24 hour trend
    // Function to group data by hour of the day and calculate the average duration
    function groupByHourOfDay(data) {
        const groupedData = {};
        data.forEach(act => {
            // Get the hour of the day (0 to 23) from the timestamp
            const date = new Date(act.created);
            const hour = date.getHours();

            // Initialize if not already in groupedData
            if (!groupedData[hour]) {
                groupedData[hour] = { totalDuration: 0, count: 0 };
            }

            // Add duration and increment count
            groupedData[hour].totalDuration += act.duration;
            groupedData[hour].count += 1;
        });

        // Convert groupedData to an array of { x, y } format, where x is the hour (0-23)
        return Array.from({ length: 24 }, (_, hour) => ({
            x: hour, // Hour of the day
            y: groupedData[hour] ? groupedData[hour].totalDuration / groupedData[hour].count : 0
        }));
    }

    // Group the ask and tool data by hour of the day
    const groupedAskDataByHour = groupByHourOfDay(askActivities);
    const groupedToolsDataByHour = groupByHourOfDay(toolActivities);

    // Create the chart with the hourly aggregated data
    new Chart(document.getElementById('twentyFourHour'), {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Ask Duration (s)',
                    data: groupedAskDataByHour,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    fill: false,
                    tension: 0.1,
                    parsing: {
                        xAxisKey: 'x',
                        yAxisKey: 'y'
                    }
                },
                {
                    label: 'Tools Duration (s)',
                    data: groupedToolsDataByHour,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    fill: false,
                    tension: 0.1,
                    parsing: {
                        xAxisKey: 'x',
                        yAxisKey: 'y'
                    }
                }
            ]
        },
        options: { 
            scales: { 
                x: {
                    type: 'linear', // Set x-axis to linear since we're using hours (0-23)
                    ticks: {
                        stepSize: 1, // Show every hour (0 to 23)
                        callback: function(value) {
                            return value + ':00'; // Display hours as "0:00", "1:00", etc.
                        }
                    },
                    title: {
                        display: true,
                        text: 'Hour of the Day',
                        font: {
                            size: 14
                        }
                    }
                },
                y: { 
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Average Duration (s)',
                        font: {
                            size: 14
                        }
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Average Duration Per Hour of the Day',
                    font: {
                        size: 20
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                }
            }
        }
    });

     // 6. Week day trends
     // Function to group data by weekday and calculate the average duration
    function groupByWeekday(data) {
        const groupedData = {};
        data.forEach(act => {
            // Get the weekday (0 for Sunday, 1 for Monday, ..., 6 for Saturday)
            const date = new Date(act.created);
            const weekday = date.getDay(); // JavaScript's getDay returns 0 (Sunday) to 6 (Saturday)

            // Initialize if not already in groupedData
            if (!groupedData[weekday]) {
                groupedData[weekday] = { totalDuration: 0, count: 0 };
            }

            // Add duration and increment count
            groupedData[weekday].totalDuration += act.duration;
            groupedData[weekday].count += 1;
        });

        // Convert groupedData to an array of { x, y } format, where x is the weekday (0-6)
        return Array.from({ length: 7 }, (_, day) => ({
            x: day, // Weekday (0 for Sunday, ..., 6 for Saturday)
            y: groupedData[day] ? groupedData[day].totalDuration / groupedData[day].count : 0
        }));
    }

    // Group the ask and tool data by weekday
    const groupedAskDataByWeekday = groupByWeekday(askActivities);
    const groupedToolsDataByWeekday = groupByWeekday(toolActivities);

    // Create the chart with the weekday aggregated data
    new Chart(document.getElementById('weekDayTrends'), {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Ask Duration (s)',
                    data: groupedAskDataByWeekday,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    fill: false,
                    tension: 0.1,
                    parsing: {
                        xAxisKey: 'x',
                        yAxisKey: 'y'
                    }
                },
                {
                    label: 'Tools Duration (s)',
                    data: groupedToolsDataByWeekday,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    fill: false,
                    tension: 0.1,
                    parsing: {
                        xAxisKey: 'x',
                        yAxisKey: 'y'
                    }
                }
            ]
        },
        options: { 
            scales: { 
                x: {
                    type: 'linear', // Set x-axis to linear since we're using weekdays (0-6)
                    ticks: {
                        stepSize: 1, // Show every weekday
                        callback: function(value) {
                            const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
                            return weekdays[value]; // Display weekdays as labels
                        }
                    },
                    title: {
                        display: true,
                        text: 'Day of the Week',
                        font: {
                            size: 14
                        }
                    }
                },
                y: { 
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Average Duration (s)',
                        font: {
                            size: 14
                        }
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Average Duration Per Weekday',
                    font: {
                        size: 20
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                }
            }
        }
    });

});
