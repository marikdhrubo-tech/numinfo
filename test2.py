from flask import Flask, request, render_template_string
import requests
import re

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>NUMINFO | DHRUBO CYBER TRACK</title>
    <!-- Leaflet CSS + JS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #0a0c1a;
            font-family: 'Inter', 'Orbitron', sans-serif;
            overflow-x: hidden;
            color: #eef5ff;
            min-height: 100vh;
            position: relative;
        }

        /* CANVAS FOR MOUSE-MOVE PARTICLE ANIMATION */
        #particle-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            opacity: 0.9;
        }

        /* MAIN CONTENT LAYER */
        .main-content {
            position: relative;
            z-index: 2;
            width: 100%;
            min-height: 100vh;
            backdrop-filter: blur(2px);
            padding: 20px 15px 30px;
        }

        /* GLASS CARD */
        .glass-card {
            background: rgba(10, 20, 30, 0.55);
            backdrop-filter: blur(12px);
            border-radius: 32px;
            border: 1px solid rgba(0, 255, 255, 0.3);
            box-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.5), 0 0 15px rgba(0, 255, 255, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .glass-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 25px 40px -12px rgba(0, 247, 255, 0.3), 0 0 20px cyan;
        }

        .neon-text {
            text-align: center;
            font-family: 'Orbitron', monospace;
            font-weight: 800;
            font-size: 2.2rem;
            letter-spacing: 3px;
            background: linear-gradient(135deg, #aaffff, #3c8aff, #b266ff);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 10px rgba(0,255,255,0.5);
            margin-bottom: 8px;
        }

        .sub {
            text-align: center;
            font-size: 0.8rem;
            color: #7fdbff;
            letter-spacing: 1px;
            border-bottom: 1px dashed cyan;
            display: inline-block;
            width: auto;
            margin: 0 auto 15px;
        }

        .input-field {
            background: rgba(0, 0, 0, 0.6);
            border: 1.5px solid #0ff;
            border-radius: 60px;
            padding: 14px 20px;
            color: #fff;
            font-size: 1.1rem;
            font-weight: 500;
            font-family: 'Orbitron', monospace;
            text-align: center;
            letter-spacing: 1px;
            outline: none;
            transition: 0.2s;
            box-shadow: 0 0 8px rgba(0, 255, 255, 0.3);
            width: 100%;
        }

        .input-field:focus {
            border-color: #ff44dd;
            box-shadow: 0 0 20px #ff44dd, 0 0 8px cyan;
            transform: scale(1.01);
        }

        .glow-button {
            background: linear-gradient(95deg, #00c3ff, #7a2eff);
            border: none;
            border-radius: 60px;
            padding: 14px;
            font-weight: bold;
            font-size: 1.2rem;
            font-family: 'Orbitron', monospace;
            color: white;
            cursor: pointer;
            transition: 0.2s;
            letter-spacing: 2px;
            box-shadow: 0 0 12px #0ff;
            width: 100%;
            margin-top: 15px;
        }

        .glow-button:hover {
            transform: scale(1.02);
            box-shadow: 0 0 25px #0ff, 0 0 15px magenta;
            background: linear-gradient(95deg, #1ed5ff, #a14eff);
        }

        .info-panel {
            padding: 20px 22px;
            margin-top: 28px;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 28px;
            border-left: 5px solid #0ff;
        }

        .data-row {
            margin: 18px 0;
            border-bottom: 1px dashed rgba(0, 255, 255, 0.3);
            padding-bottom: 10px;
        }

        .data-label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #0ff;
            font-weight: 500;
        }

        .data-value {
            font-size: 1.2rem;
            font-weight: bold;
            word-break: break-word;
            color: #f0fcff;
            text-shadow: 0 0 4px cyan;
        }

        .map-container {
            margin-top: 28px;
            border-radius: 28px;
            overflow: hidden;
            border: 2px solid rgba(0, 255, 255, 0.6);
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
            height: 280px;
            background: #111;
        }

        #map {
            height: 100%;
            width: 100%;
            z-index: 3;
        }

        .distance-badge {
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(12px);
            border-radius: 40px;
            padding: 10px 18px;
            text-align: center;
            margin-top: 18px;
            font-weight: bold;
            font-size: 1.1rem;
            border: 1px solid cyan;
            color: #afff;
        }

        .footer {
            margin-top: 40px;
            text-align: center;
            padding: 20px 10px 10px;
            font-size: 0.8rem;
            border-top: 1px solid rgba(0, 255, 255, 0.3);
        }

        .insta-link {
            color: #ff66cc;
            text-decoration: none;
            font-weight: bold;
            transition: 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .insta-link:hover {
            text-shadow: 0 0 8px magenta;
            color: #ff99ff;
            transform: scale(1.02);
        }

        @keyframes fadeSlideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .animate-page {
            animation: fadeSlideUp 0.6s ease-out forwards;
        }

        .credit {
            font-family: monospace;
            font-weight: bold;
            background: linear-gradient(135deg, cyan, magenta);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        @media (max-width: 550px) {
            .neon-text {
                font-size: 1.6rem;
            }
            .data-value {
                font-size: 1rem;
            }
        }
    </style>
</head>
<body>

<canvas id="particle-canvas"></canvas>

<div class="main-content">
    <div style="max-width: 650px; margin: 0 auto;">
        <!-- HEADER -->
        <div class="glass-card" style="padding: 18px 20px; text-align: center; margin-bottom: 20px;">
            <div class="neon-text">☠ NUMINFO BY DHRUBO ☠</div>
            <div class="sub">✦ LIVE GEOLOCATION TRACKER ✦</div>
        </div>

        <!-- SEARCH CARD -->
        <div class="glass-card" style="padding: 28px 22px;">
            <form method="POST" id="searchForm">
                <input type="text" name="number" class="input-field" placeholder="🔢 ENTER TARGET NUMBER" required autocomplete="off">
                <button type="submit" class="glow-button">⚡ ACCESS INTELL ⚡</button>
            </form>
        </div>

        <!-- RESULT AREA (ENHANCED WITH ALL FIELDS) -->
        {% if data %}
        <div class="info-panel animate-page" id="infoBlock">
            <div style="text-align: center; margin-bottom: 10px;">
                <span style="background: #0ff22e30; padding: 5px 12px; border-radius: 30px;">🎯 TARGET ACQUIRED</span>
            </div>
            <div class="data-row">
                <div class="data-label">👤 NAME</div>
                <div class="data-value">{{ data.name }}</div>
            </div>
            <div class="data-row">
                <div class="data-label">👨‍👦 FATHER NAME</div>
                <div class="data-value">{{ data.father_name }}</div>
            </div>
            <div class="data-row">
                <div class="data-label">📱 MOBILE</div>
                <div class="data-value">{{ data.mobile }}</div>
            </div>
            <div class="data-row">
                <div class="data-label">🏠 ADDRESS</div>
                <div class="data-value" id="targetAddressRaw">{{ data.address }}</div>
            </div>
            <div class="data-row">
                <div class="data-label">📡 CIRCLE</div>
                <div class="data-value">{{ data.circle }}</div>
            </div>
            <div class="data-row">
                <div class="data-label">🪪 AADHAAR</div>
                <div class="data-value">{{ data.aadhaar }}</div>
            </div>
        </div>
        {% else %}
        <div class="glass-card" style="padding: 20px; text-align: center; margin-top: 20px; background: rgba(0,0,0,0.4);">
            <span style="color: #88ccff;">⚡ ENTER NUMBER TO EXTRACT INFORMATION ⚡</span>
        </div>
        {% endif %}

        <!-- MAP SECTION -->
        <div class="glass-card" style="padding: 10px; margin-top: 25px;">
            <div style="margin-left: 5px; font-weight: bold; margin-bottom: 8px;">🗺️ LIVE TRACKING MAP</div>
            <div class="map-container">
                <div id="map"></div>
            </div>
            <div id="distanceDisplay" class="distance-badge">📍 waiting for target data...</div>
        </div>

        <!-- FOOTER WITH DEVELOPER CREDIT AND INSTAGRAM -->
        <div class="footer">
            <p>⚡ DEVELOPED BY <span class="credit">DHRUBO</span> ⚡</p>
            <p style="margin-top: 8px;">
                <a href="https://instagram.com/g.3y6" target="_blank" class="insta-link">
                    📸 INSTAGRAM : @g.3y6
                </a>
            </p>
            <p style="font-size: 10px; opacity: 0.7; margin-top: 12px;">cyber intel | reactive particle interface</p>
        </div>
    </div>
</div>

<script>
    // ========== MOUSE-MOVE PARTICLE ANIMATION ==========
    const canvas = document.getElementById('particle-canvas');
    let ctx = canvas.getContext('2d');
    let width = window.innerWidth;
    let height = window.innerHeight;
    let particles = [];
    let mouseX = width/2, mouseY = height/2;
    let mousePresent = false;

    const PARTICLE_COUNT = 120;
    const CONNECTION_DIST = 150;
    const MOUSE_RADIUS = 110;
    const REPULSION_FORCE = 0.9;

    class Particle {
        constructor(x, y) {
            this.x = x;
            this.y = y;
            this.vx = (Math.random() - 0.5) * 0.6;
            this.vy = (Math.random() - 0.5) * 0.6;
            this.size = Math.random() * 2.8 + 1.2;
            this.baseX = x;
            this.baseY = y;
            this.color = `hsl(${Math.random() * 60 + 170}, 85%, 65%)`;
        }
        
        update() {
            if (mousePresent) {
                let dx = this.x - mouseX;
                let dy = this.y - mouseY;
                let dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < MOUSE_RADIUS) {
                    let angle = Math.atan2(dy, dx);
                    let force = (MOUSE_RADIUS - dist) / MOUSE_RADIUS;
                    let pushX = Math.cos(angle) * force * REPULSION_FORCE;
                    let pushY = Math.sin(angle) * force * REPULSION_FORCE;
                    this.vx += pushX;
                    this.vy += pushY;
                }
            }
            
            let toBaseX = (this.baseX - this.x) * 0.008;
            let toBaseY = (this.baseY - this.y) * 0.008;
            this.vx += toBaseX;
            this.vy += toBaseY;
            
            this.vx *= 0.96;
            this.vy *= 0.96;
            
            this.x += this.vx;
            this.y += this.vy;
            
            if (this.x < 0) { this.x = 0; this.vx *= -0.5; }
            if (this.x > width) { this.x = width; this.vx *= -0.5; }
            if (this.y < 0) { this.y = 0; this.vy *= -0.5; }
            if (this.y > height) { this.y = height; this.vy *= -0.5; }
        }
        
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.shadowBlur = 8;
            ctx.shadowColor = "#0ff";
            ctx.fill();
            ctx.shadowBlur = 0;
        }
    }
    
    function initParticles() {
        particles = [];
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            let x = Math.random() * width;
            let y = Math.random() * height;
            particles.push(new Particle(x, y));
        }
    }
    
    function drawConnections() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i+1; j < particles.length; j++) {
                let dx = particles[i].x - particles[j].x;
                let dy = particles[i].y - particles[j].y;
                let dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < CONNECTION_DIST) {
                    let opacity = (1 - dist/CONNECTION_DIST) * 0.4;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(0, 210, 255, ${opacity+0.15})`;
                    ctx.lineWidth = 1.2;
                    ctx.stroke();
                }
            }
        }
    }
    
    function animateParticles() {
        if (!ctx) return;
        ctx.clearRect(0, 0, width, height);
        let grad = ctx.createLinearGradient(0, 0, width, height);
        grad.addColorStop(0, '#02061720');
        grad.addColorStop(1, '#0a0c1a30');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, width, height);
        
        for (let p of particles) {
            p.update();
            p.draw();
        }
        drawConnections();
        
        if (mousePresent) {
            ctx.beginPath();
            ctx.arc(mouseX, mouseY, 28, 0, Math.PI*2);
            ctx.fillStyle = '#00ffff15';
            ctx.shadowBlur = 18;
            ctx.fill();
            ctx.beginPath();
            ctx.arc(mouseX, mouseY, 12, 0, Math.PI*2);
            ctx.fillStyle = '#ff44dd25';
            ctx.fill();
            ctx.shadowBlur = 0;
        }
        
        requestAnimationFrame(animateParticles);
    }
    
    function resizeCanvas() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
        initParticles();
    }
    
    window.addEventListener('resize', () => resizeCanvas());
    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        mousePresent = true;
    });
    window.addEventListener('mouseleave', () => { mousePresent = false; });
    
    resizeCanvas();
    animateParticles();
    
    // ========== LEAFLET MAP AND GEOLOCATION ==========
    let mapInstance = null;
    let currentTargetMarker = null;
    let currentUserMarker = null;
    let currentPolyline = null;
    let userLatLng = null;
    
    function initMap() {
        if (mapInstance) mapInstance.remove();
        mapInstance = L.map('map').setView([20.5937, 78.9629], 5);
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> & CartoDB',
            subdomains: 'abcd',
            maxZoom: 18
        }).addTo(mapInstance);
    }
    
    function getUserLocation() {
        return new Promise((resolve) => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition((pos) => {
                    userLatLng = { lat: pos.coords.latitude, lng: pos.coords.longitude };
                    if (currentUserMarker) mapInstance.removeLayer(currentUserMarker);
                    currentUserMarker = L.marker([userLatLng.lat, userLatLng.lng], {
                        icon: L.divIcon({ html: '📍', iconSize: [20,20], className: 'custom-marker-icon' })
                    }).addTo(mapInstance).bindPopup('<b>YOU</b> (your device)').openPopup();
                    resolve(userLatLng);
                }, () => resolve(null));
            } else resolve(null);
        });
    }
    
    async function geocodeAddress(addressStr) {
        if (!addressStr || addressStr === "N/A" || addressStr.length < 5) return null;
        try {
            const resp = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(addressStr)}&limit=1`);
            const data = await resp.json();
            if (data && data.length) return { lat: parseFloat(data[0].lat), lon: parseFloat(data[0].lon) };
        } catch(e) { console.error(e); }
        return null;
    }
    
    function calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371;
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180) * Math.cos(lat2*Math.PI/180) * Math.sin(dLon/2)**2;
        return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    }
    
    async function updateMapWithAddress(address) {
        if (!mapInstance) initMap();
        if (currentTargetMarker) mapInstance.removeLayer(currentTargetMarker);
        if (currentPolyline) mapInstance.removeLayer(currentPolyline);
        document.getElementById('distanceDisplay').innerHTML = "📍 calculating distance & target location...";
        
        const coords = await geocodeAddress(address);
        if (!coords) {
            document.getElementById('distanceDisplay').innerHTML = "⚠️ Could not geolocate address.";
            return;
        }
        
        const targetIcon = L.divIcon({ html: '🎯', iconSize: [25,25], className: 'target-icon' });
        currentTargetMarker = L.marker([coords.lat, coords.lon], { icon: targetIcon }).addTo(mapInstance)
            .bindPopup(`<b>TARGET</b><br>${address.substring(0, 80)}`).openPopup();
        
        if (!userLatLng) await getUserLocation();
        
        if (userLatLng) {
            const dist = calculateDistance(userLatLng.lat, userLatLng.lng, coords.lat, coords.lon);
            document.getElementById('distanceDisplay').innerHTML = `📏 DISTANCE FROM YOU: ${dist.toFixed(2)} KM 📏`;
            currentPolyline = L.polyline([[userLatLng.lat, userLatLng.lng], [coords.lat, coords.lon]], {
                color: '#0ff', weight: 3, opacity: 0.8, dashArray: '8, 8'
            }).addTo(mapInstance);
            mapInstance.fitBounds(L.latLngBounds([userLatLng, {lat: coords.lat, lng: coords.lon}]), { padding: [40,40] });
        } else {
            document.getElementById('distanceDisplay').innerHTML = `📍 TARGET LOCATION: ${coords.lat.toFixed(4)}, ${coords.lon.toFixed(4)} (enable location for distance)`;
            mapInstance.setView([coords.lat, coords.lon], 12);
        }
    }
    
    window.addEventListener('load', () => {
        initMap();
        getUserLocation();
        {% if data %}
            const addrElem = document.getElementById('targetAddressRaw');
            if (addrElem && addrElem.innerText && addrElem.innerText !== "N/A") {
                setTimeout(() => updateMapWithAddress(addrElem.innerText), 500);
            } else {
                document.getElementById('distanceDisplay').innerHTML = "❓ Address not found in API response";
            }
        {% endif %}
    });
</script>
</body>
</html>
"""

def fetch_data(number):
    """
    Fetch and parse the API response to extract:
    - Name
    - Father Name
    - Mobile (same as input)
    - Address
    - Circle (e.g., AIRTEL WB)
    - Aadhaar number
    """
    try:
        url = f"https://exploitsindia.site/track/live.php?term={number}"
        res = requests.get(url, timeout=10).text
        
        # Helper to extract data using regex patterns (case-insensitive)
        def extract(pattern, default="N/A"):
            match = re.search(pattern, res, re.IGNORECASE | re.DOTALL)
            if match:
                # Clean up extra whitespace and newlines
                return re.sub(r'\s+', ' ', match.group(1)).strip()
            return default
        
        # Patterns based on typical API response structure
        name = extract(r"Name[:\-]?\s*(.*?)(?:\n|\r|$|<br)", "N/A")
        father = extract(r"Father(?:'s)?\s*Name[:\-]?\s*(.*?)(?:\n|\r|$|<br)", "N/A")
        # Address may span multiple lines until next field
        address = extract(r"Address[:\-]?\s*(.*?)(?:(?:Circle|Aadhaar|Mobile)|\n\n|$)", "N/A")
        circle = extract(r"Circle[:\-]?\s*(.*?)(?:\n|\r|$|<br)", "N/A")
        aadhaar = extract(r"Aadhaar[:\-]?\s*(\d{12}|\d{4}\s*\d{4}\s*\d{4}|\S+)", "N/A")
        
        # Clean up Aadhaar formatting (remove spaces if any)
        if aadhaar != "N/A":
            aadhaar = re.sub(r'\s', '', aadhaar)
        
        # If address extraction gave too long or includes other keywords, trim
        if "Circle" in address or "Aadhaar" in address:
            address = address.split("Circle")[0].split("Aadhaar")[0].strip()
        
        return {
            "name": name if name != "N/A" else "Not Found",
            "father_name": father,
            "mobile": number,
            "address": address,
            "circle": circle,
            "aadhaar": aadhaar
        }
    except Exception as e:
        print(f"API Error: {e}")
        return None

@app.route("/", methods=["GET","POST"])
def home():
    data = None
    if request.method == "POST":
        number = request.form.get("number")
        data = fetch_data(number)
    return render_template_string(HTML, data=data)

if __name__ == "__main__":
    print("""
          
██████╗ ██╗  ██╗██████╗ ██╗   ██╗██████╗  ██████╗ 
██╔══██╗██║  ██║██╔══██╗██║   ██║██╔══██╗██╔═══██╗
██║  ██║███████║██████╔╝██║   ██║██████╔╝██║   ██║
██║  ██║██╔══██║██╔══██╗██║   ██║██╔══██╗██║   ██║
██████╔╝██║  ██║██║  ██║╚██████╔╝██████╔╝╚██████╔╝
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝
          
━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ DEVELOPER BY DHRUBO ⚡
━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    app.run(host="0.0.0.0", port=5000, debug=True)