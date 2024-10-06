const mqtt = require("mqtt");
const client = mqtt.connect("http://127.0.0.1:1883");

// Simulating data publishing from thousands of weather stations
function publishWeatherData(stationId) {
    const data = {
        stationId: stationId,
        timestamp: Date.now(),
        temperature: (Math.random() * 45).toFixed(2),  // Simulating temperature between 0 and 40 degrees Celsius
        humidity: (Math.random() * 100).toFixed(2),    // Humidity percentage
        windSpeed: (Math.random() * 100).toFixed(2),    // Wind speed in km/h
        pressure: (Math.random() * 20 + 980).toFixed(2) // Atmospheric pressure in hPa (980-1000)
    };

    const topic = `weather/stations/${stationId}`;
    const message = JSON.stringify(data);
    
    client.publish(topic, message, { qos: 2 }, (err) => {
        if (err) {
            console.error(`Failed to publish data from station ${stationId}:`, err);
        } else {
            console.log(`Published weather data from station ${stationId}`);
        }
    });
}

// Simulating 10,000 weather stations sending data every 5 seconds
setInterval(() => {
    for (let i = 1; i <= 10000; i++) {
        publishWeatherData(i);
    }
}, 3000);

// Handle MQTT connection events
client.on('connect', () => {
    console.log('Connected to MQTT broker');
});

client.on('error', (err) => {
    console.error('MQTT connection error:', err);
});
