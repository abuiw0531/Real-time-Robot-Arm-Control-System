// Connect to Flask-SocketIO Server
const socket = io();

// DOM Elements
const apertureTextLive = document.getElementById('live-aperture');
const gaugeValue = document.getElementById('gauge-value');
const gaugeProgress = document.getElementById('gauge-progress');
const statusTag = document.getElementById('status-tag');
const commandList = document.getElementById('command-list');
const fpsBadge = document.getElementById('fps-badge');
const connectionText = document.getElementById('connection-text');
const connectionDot = document.getElementById('connection-dot');

const dashArray = 125.6;
let lastApertureStatus = 0; // 0 is safe, 1 is triggered

// Connection Events
socket.on('connect', () => {
    connectionText.textContent = 'System Active';
    connectionDot.classList.add('online');
    connectionDot.style.backgroundColor = 'var(--accent-primary)';
});

socket.on('disconnect', () => {
    connectionText.textContent = 'Disconnected';
    connectionDot.classList.remove('online');
    connectionDot.style.backgroundColor = 'var(--accent-danger)';
});

// Real-time Data received from Python backend
socket.on('update_data', (data) => {
    // data: { aperture: float, raw_commands: array, a_status: int, latency: float, fps: int }
    
    // Update FPS
    if (data.fps !== undefined) {
        fpsBadge.textContent = `FPS: ${data.fps}`;
    }

    // Update Aperture Gauge
    const currentAperture = typeof data.aperture === 'number' && !isNaN(data.aperture) ? data.aperture : 0;
    apertureTextLive.textContent = currentAperture.toFixed(2);
    
    // Convert aperture (assumed max useful value is typical hand size ~1.0) to percentage
    const percentage = Math.min(Math.max(currentAperture * 100, 0), 100);
    gaugeValue.textContent = `${Math.round(percentage)}%`;

    const strokeOffset = dashArray - (dashArray * (percentage / 100));
    gaugeProgress.style.strokeDashoffset = strokeOffset;

    // Logic: Threshold Check (Driven by backend status `a_status`)
    // a_status == 1 means triggered (aperture < threshold)
    const triggered = data.a_status === 1;
    
    if (triggered) {
        // Danger state (Aperture triggering 'A')
        gaugeProgress.style.stroke = 'var(--accent-danger)';
        apertureTextLive.style.color = 'var(--accent-danger)';
        statusTag.textContent = 'TRIGGERED';
        statusTag.className = 'status-tag danger';
    } else {
        // Safe state
        gaugeProgress.style.stroke = 'var(--accent-primary)';
        apertureTextLive.style.color = 'var(--accent-primary)';
        statusTag.textContent = 'SAFE';
        statusTag.className = 'status-tag safe';
    }

    // Log Commands if any
    if (data.raw_commands && data.raw_commands.length > 0) {
        data.raw_commands.forEach(cmdList => {
            // cmdList is [action, speed, a_status] e.g. ['L', 0.2, 0] or ['A', 0, 1]
            const action = cmdList[0];
            const speedStr = typeof cmdList[1] === 'number' ? cmdList[1].toFixed(2) : cmdList[1];
            const a_stat = cmdList[2];
            
            const message = `Cmd: (${action}, ${speedStr}, ${a_stat})`;
            addLogEntry(action, message);
        });
    } else if (data.has_hands) {
        // If center
        if (data.a_status !== lastApertureStatus) {
            // implicit A status change
        } else {
            // Do not spam center logs every frame, or do it with throttling
            // addLogEntry('Center', `Cmd: (Center, 1, 0)`);
        }
    }
    
    lastApertureStatus = data.a_status;
});

function addLogEntry(action, message) {
    const li = document.createElement('li');
    const timeSpan = document.createElement('span');
    timeSpan.className = 'time mono';
    
    const now = new Date();
    timeSpan.textContent = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
    
    const msgSpan = document.createElement('span');
    if (action === 'A') {
        msgSpan.className = 'cmd action';
    } else {
        msgSpan.className = 'cmd fw';
    }
    msgSpan.textContent = message;
    
    li.appendChild(timeSpan);
    li.appendChild(msgSpan);
    
    commandList.prepend(li);
    
    // keep more items since it's now horizontal grid layout in the bottom
    if (commandList.children.length > 20) {
        commandList.removeChild(commandList.lastChild);
    }
}

// System controls
function shutdownServer() {
    if(confirm("確定要關閉伺服器與控制程式嗎？")) {
        fetch('/shutdown', { method: 'POST' })
            .then(() => {
                document.body.innerHTML = '<div style="display: flex; height: 100vh; justify-content: center; align-items: center; background: #000; color: #fff; flex-direction: column;"><h2>系統已關閉</h2><p>您可以安全地關閉此網頁。</p></div>';
            });
    }
}
