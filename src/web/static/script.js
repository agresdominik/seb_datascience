const socket = io();

// Listen for updates from the server
socket.on('update', (data) => {
    document.getElementById('temperature').textContent = data.temperature.toFixed(1);
    document.getElementById('window_time').textContent = data.window_time;
    document.getElementById('temperature_outside').textContent = data.temperature_outside.toFixed(1);
});

