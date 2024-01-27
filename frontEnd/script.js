function getData() {
    return Math.random();
}

// Create an initial trace
Plotly.plot("chart", [{
    y: [getData()],
    type: 'line'
}]);

// Update the chart every 250 milliseconds
setInterval(function(){
    Plotly.extendTraces('chart', {y: [[getData()]]}, [0]);
}, 250);
