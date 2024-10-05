const mqtt = require('mqtt');
const client = mqtt.connect('http://127.0.0.1');  // Replace with your broker address

// Subscribe to the relevant topics
client.on('connect', () => {
    console.log('Connected to MQTT broker');
    client.subscribe('weather/stations/#', (err) => {
        if (err) {
            console.error('Subscription error:', err);
        } else {
            console.log('Subscribed to weather stations data');
        }
    });
});

// Handle incoming messages
client.on('message', (topic, message) => {
    const weatherData = JSON.parse(message.toString());
    const { stationId, temperature, windSpeed,pressure } = weatherData;

    // Example alert conditions
    if (temperature > 44) {
        console.log('Alert: High temperature detected at station ${stationId}');
        console.log('temperature',temperature);
        console.log('\n');
        console.log('\n');
        console.log('\n');
        // Trigger an alert, e.g., send an email or SMS
    }

    if (windSpeed > 99 && pressure > 999) {
        console.log('Alert: High wind speed detected at station ${stationId}');
        console.log('windSpeed',windSpeed);
        console.log('pressure',pressure);
        console.log('\n');
        console.log('\n');
        console.log('\n');

        // Trigger an alert, e.g., send an email or SMS
    }
});

// Handle errors
client.on('error', (err) => {
    console.error('MQTT connection error:', err);
});