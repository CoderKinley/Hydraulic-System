// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.2/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.7.2/firebase-analytics.js";
import { getDatabase, ref, onValue } from "https://www.gstatic.com/firebasejs/10.7.2/firebase-database.js";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "pyto-db701.firebaseapp.com",
    databaseURL: "https://pyto-db701-default-rtdb.firebaseio.com",
    projectId: "pyto-db701",
    storageBucket: "pyto-db701.appspot.com",
    messagingSenderId: "229412264516",
    appId: "1:229412264516:web:f2fdafadec99efeef23a11",
    measurementId: "G-PYES5CSJQ7"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Get a reference to the database
const database = getDatabase(app);

// Listen for value changes in the database
onValue(ref(database), (snapshot) => {
    const data = snapshot.val();
    if (data) {
        // Update the HTML content with real-time data in table format
        // updateRealTimeDataTable(data);
        // Update the chart with real-time data
        updateRealTimeChart(data);
    }
    else {
        console.log("No data found in Realtime Database");
    }
}, {
    onlyOnce: false
});

// Initialize an empty trace
Plotly.plot("chart", [{
    x: [],
    y: [],
    type: 'line',
    name: 'Piston Extension',
}]);

// Function to update the chart with real-time data
function updateRealTimeChart(data) {
    const timeArray = [];
    const pistonExtensionArray = [];

    // Assuming 0.25s intervals and maintaining the order of data
    let currentTime = 0;
    Object.keys(data).forEach(key => {
        timeArray.push(currentTime);
        pistonExtensionArray.push(data[key].Piston_extension);
        currentTime += 0.25;  // Increment time for each data point
    });

    const chartData = {
        x: [timeArray],
        y: [pistonExtensionArray],
    };

    // Update the chart
    Plotly.update("chart", chartData, [0]);
}
