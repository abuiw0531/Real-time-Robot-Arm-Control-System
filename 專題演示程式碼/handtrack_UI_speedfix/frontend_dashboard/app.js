// Simulate real-time data from the robot arm
const config = {
    threshold: 0.20,
    updateIntervalMs: 100 // 10fps fake data update
};

// DOM Elements
const apertureTextLive = document.getElementById('live-aperture');
const gaugeValue = document.querySelector('.gauge-value');
const gaugeProgress = document.querySelector('.gauge-progress');
const statusTag = document.querySelector('.status-tag');
const trackingBox = document.querySelector('.tracking-box');
const commandList = document.getElementById('command-list');

// Internal State
let currentAperture = 0.45;
let isApertureTriggered = false;

// Geometry helpers for gauge (stroke-dasharray="125.6")
// length of arc = pi * r = 3.14 * 40 = 125.6
const dashArray = 125.6;

function updateDashboardUI() {
    // 1. Update Texts
    const displayVal = currentAperture.toFixed(2);
    apertureTextLive.textContent = displayVal;
    
    // Percentage for gauge
    const percentage = Math.min(Math.max(currentAperture * 100, 0), 100);
    gaugeValue.textContent = `${Math.round(percentage)}%`;

    // 2. Update Gauge Arc
    // offset ranges from 125.6 (empty) to 0 (full)
    const strokeOffset = dashArray - (dashArray * (percentage / 100));
    gaugeProgress.style.strokeDashoffset = strokeOffset;

    // 3. Logic: Threshold Check
    const triggered = currentAperture < config.threshold;
    
    if (triggered !== isApertureTriggered) {
        isApertureTriggered = triggered;
        
        // State changed
        if (triggered) {
            // Danger state
            gaugeProgress.style.stroke = 'var(--accent-danger)';
            apertureTextLive.style.color = 'var(--accent-danger)';
            statusTag.textContent = 'TRIGGERED';
            statusTag.className = 'status-tag danger';
            trackingBox.style.borderColor = 'var(--accent-danger)';
            trackingBox.style.boxShadow = '0 0 15px var(--accent-danger-glow), inset 0 0 10px var(--accent-danger-glow)';
            
            addLogEntry('A', 'Cmd: (A, 0, 1)');
        } else {
            // Safe state
            gaugeProgress.style.stroke = 'var(--accent-primary)';
            apertureTextLive.style.color = 'var(--accent-primary)';
            statusTag.textContent = 'SAFE';
            statusTag.className = 'status-tag safe';
            trackingBox.style.borderColor = 'var(--accent-primary)';
            trackingBox.style.boxShadow = '0 0 15px var(--accent-primary-glow), inset 0 0 10px var(--accent-primary-glow)';
            
            addLogEntry('A', 'Cmd: (A, 0, 0)');
        }
    }
}

function addLogEntry(type, message) {
    const li = document.createElement('li');
    const timeSpan = document.createElement('span');
    timeSpan.className = 'time mono';
    
    const now = new Date();
    timeSpan.textContent = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
    
    const msgSpan = document.createElement('span');
    // Basic coloring based on fake types
    if (message.includes('A,')) msgSpan.className = 'cmd action';
    else msgSpan.className = 'cmd fw';
    msgSpan.textContent = message;
    
    li.appendChild(timeSpan);
    li.appendChild(msgSpan);
    
    commandList.prepend(li);
    
    // keep only 10 items
    if (commandList.children.length > 5) {
        commandList.removeChild(commandList.lastChild);
    }
}

// Data simulation loop
setInterval(() => {
    // Add some random noise to emulate hand shaking
    let noise = (Math.random() - 0.5) * 0.05;
    
    // Randomly move towards threshold every few seconds
    if (Math.random() > 0.95) {
        // Big shift
        currentAperture = Math.random() > 0.5 ? 0.15 : 0.60;
    } else {
        // Slow drift
        currentAperture += noise;
    }

    // Clamp values 0 to 1
    currentAperture = Math.max(0.05, Math.min(1.0, currentAperture));
    
    updateDashboardUI();
    
    // Random movement logs
    if (Math.random() > 0.9 && !isApertureTriggered) {
        const dirs = ['F', 'B', 'L', 'R', 'Center'];
        const speed = Math.floor(Math.random() * 5) + 1;
        const dir = dirs[Math.floor(Math.random() * dirs.length)];
        if(dir === 'Center') {
            addLogEntry(dir, `Cmd: (${dir}, 1, 0)`);
        } else {
            addLogEntry(dir, `Cmd: (${dir}, ${speed}, 0)`);
        }
    }
    
}, config.updateIntervalMs);

// Initialize
updateDashboardUI();
