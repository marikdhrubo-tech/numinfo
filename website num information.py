from flask import Flask, render_template_string, request
import requests
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile Number Lookup System | DHRUBO</title>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
            cursor: none;
        }

        /* Custom Cursor */
        .cursor {
            position: fixed;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.8);
            pointer-events: none;
            z-index: 9999;
            transition: transform 0.1s;
            mix-blend-mode: difference;
        }

        .cursor-follower {
            position: fixed;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: 2px solid rgba(255, 255, 255, 0.5);
            pointer-events: none;
            z-index: 9998;
            transition: all 0.2s;
            mix-blend-mode: difference;
        }

        /* Floating Particles */
        .particle {
            position: fixed;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 50%;
            pointer-events: none;
            z-index: 1;
            animation: floatParticle linear infinite;
        }

        @keyframes floatParticle {
            0% {
                transform: translateY(100vh) translateX(0);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100px) translateX(50px);
                opacity: 0;
            }
        }

        /* Glow Effect */
        .glow {
            position: fixed;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
            pointer-events: none;
            z-index: 0;
            border-radius: 50%;
            transform: translate(-50%, -50%);
        }

        /* Main Container */
        .container {
            position: relative;
            z-index: 2;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        /* Card */
        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            width: 100%;
            max-width: 1000px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: fadeInUp 0.8s ease;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Header */
        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            color: white;
            font-size: 2.5em;
            margin-bottom: 10px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% {
                text-shadow: 0 0 10px rgba(255,255,255,0.5);
            }
            50% {
                text-shadow: 0 0 20px rgba(255,255,255,0.8);
            }
        }

        .header p {
            color: rgba(255, 255, 255, 0.8);
            font-size: 1.1em;
        }

        /* Input Group */
        .input-group {
            margin-bottom: 20px;
        }

        .input-wrapper {
            position: relative;
            display: flex;
            align-items: center;
        }

        .country-code {
            position: absolute;
            left: 15px;
            color: #667eea;
            font-weight: bold;
            font-size: 16px;
            pointer-events: none;
        }

        input {
            width: 100%;
            padding: 15px;
            padding-left: 50px;
            border: none;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            transition: all 0.3s;
            outline: none;
        }

        input:focus {
            transform: scale(1.02);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        button {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }

        button:active {
            transform: translateY(0);
        }

        /* Loading Animation */
        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
        }

        .loading.active {
            display: block;
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(255,255,255,0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Success Message */
        .success-message {
            background: rgba(72, 187, 120, 0.2);
            border: 1px solid rgba(72, 187, 120, 0.5);
            border-radius: 10px;
            padding: 15px;
            color: #48bb78;
            text-align: center;
            margin-top: 20px;
            animation: slideIn 0.5s ease;
        }

        /* Query Info */
        .query-info {
            background: rgba(102, 126, 234, 0.2);
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }

        .query-badge {
            background: rgba(102, 126, 234, 0.3);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 14px;
        }

        .total-results {
            background: #667eea;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }

        /* Results */
        .results {
            margin-top: 30px;
            animation: slideIn 0.5s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .result-card {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            transition: all 0.3s;
            border-left: 4px solid #667eea;
        }

        .result-card:hover {
            transform: translateX(5px);
            background: rgba(255, 255, 255, 0.2);
        }

        .result-title {
            font-size: 18px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }

        .result-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }

        .result-item {
            display: flex;
            flex-direction: column;
        }

        .result-label {
            font-size: 12px;
            color: #a0aec0;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }

        .result-value {
            font-size: 16px;
            color: white;
            font-weight: 500;
            word-break: break-word;
        }

        .result-value.null {
            color: #a0aec0;
            font-style: italic;
        }

        .highlight {
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
            font-weight: bold;
        }

        /* Error Message */
        .error {
            background: rgba(255, 68, 68, 0.2);
            border: 1px solid rgba(255, 68, 68, 0.5);
            border-radius: 10px;
            padding: 15px;
            color: #ff6b6b;
            text-align: center;
            margin-top: 20px;
        }

        /* Footer */
        .footer {
            position: fixed;
            bottom: 20px;
            left: 0;
            right: 0;
            text-align: center;
            z-index: 10;
        }

        .instagram-btn {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: linear-gradient(45deg, #f09433, #d62976, #962fbf);
            padding: 12px 25px;
            border-radius: 50px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-5px);
            }
        }

        .instagram-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }

        .developer {
            text-align: center;
            margin-top: 20px;
            padding-top: 20px;
            color: rgba(255, 255, 255, 0.7);
            font-size: 14px;
            border-top: 1px solid rgba(255,255,255,0.2);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .card {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 1.5em;
            }
            
            .result-grid {
                grid-template-columns: 1fr;
            }
            
            .query-info {
                flex-direction: column;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <div class="cursor"></div>
    <div class="cursor-follower"></div>
    <div class="glow" id="glow"></div>

    <div class="container">
        <div class="card">
            <div class="header">
                <h1>📱 Mobile Number Lookup System</h1>
                <p>Enter any mobile number to find associated information</p>
            </div>

            <form method="POST" id="searchForm">
                <div class="input-group">
                    <div class="input-wrapper">
                        <span class="country-code">+91</span>
                        <input 
                            type="tel" 
                            name="number" 
                            placeholder="Enter 10-digit mobile number" 
                            required
                            pattern="[0-9]{10}"
                            maxlength="10"
                            autocomplete="off">
                    </div>
                    <small style="color: rgba(255,255,255,0.7); display: block; margin-top: 5px;">
                        Enter 10-digit mobile number (without country code)
                    </small>
                </div>
                <button type="submit">
                    🔍 Search Now
                </button>
            </form>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="color: white; margin-top: 10px;">Searching database...</p>
            </div>

            {% if error %}
            <div class="error">
                <strong>⚠️ Error:</strong> {{ error }}
            </div>
            {% endif %}

            {% if message %}
            <div class="success-message">
                ✅ {{ message }}
            </div>
            {% endif %}

            {% if query_type and query_value %}
            <div class="query-info">
                <span class="query-badge">🔍 Query Type: {{ query_type|upper }}</span>
                <span class="query-badge">📱 Query Value: {{ query_value }}</span>
                <span class="total-results">📊 Total Results: {{ total_results }}</span>
            </div>
            {% endif %}

            {% if results %}
            <div class="results">
                <h3 style="color: white; margin-bottom: 15px;">📋 Search Results</h3>
                {% for result in results %}
                <div class="result-card">
                    <div class="result-title">
                        Result #{{ loop.index }}
                    </div>
                    <div class="result-grid">
                        {% if result.name %}
                        <div class="result-item">
                            <div class="result-label">👤 Name</div>
                            <div class="result-value">{{ result.name }}</div>
                        </div>
                        {% endif %}
                        
                        {% if result.mobile %}
                        <div class="result-item">
                            <div class="result-label">📱 Mobile Number</div>
                            <div class="result-value">{{ result.mobile }}</div>
                        </div>
                        {% endif %}
                        
                        {% if result.fname %}
                        <div class="result-item">
                            <div class="result-label">👨 Father's Name</div>
                            <div class="result-value">{{ result.fname }}</div>
                        </div>
                        {% endif %}
                        
                        {% if result.address %}
                        <div class="result-item">
                            <div class="result-label">🏠 Address</div>
                            <div class="result-value">{{ result.address.replace('!', ', ') }}</div>
                        </div>
                        {% endif %}
                        
                        {% if result.circle %}
                        <div class="result-item">
                            <div class="result-label">📡 Circle/Operator</div>
                            <div class="result-value">{{ result.circle }}</div>
                        </div>
                        {% endif %}
                        
                        {% if result.id %}
                        <div class="result-item">
                            <div class="result-label">🆔 ID</div>
                            <div class="result-value">{{ result.id }}</div>
                        </div>
                        {% endif %}
                        
                        {% if result.email %}
                        <div class="result-item">
                            <div class="result-label">📧 Email</div>
                            <div class="result-value">{{ result.email }}</div>
                        </div>
                        {% else %}
                        <div class="result-item">
                            <div class="result-label">📧 Email</div>
                            <div class="result-value null">Not available</div>
                        </div>
                        {% endif %}
                        
                        {% if result.alt %}
                        <div class="result-item">
                            <div class="result-label">🔄 Alternative</div>
                            <div class="result-value">{{ result.alt }}</div>
                        </div>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endif %}

            {% if highlight %}
            <div class="highlight">
                🔥 {{ highlight }}
            </div>
            {% endif %}

            <div class="developer">
                Developed by <strong style="color: #667eea;">DHRUBO</strong>
            </div>
        </div>
    </div>

    <div class="footer">
        <a href="https://instagram.com/g.3y6" target="_blank" class="instagram-btn">
            <span>📷</span>
            Follow on Instagram
            <span>✨</span>
        </a>
    </div>

    <script>
        // Mouse Move Animation
        const cursor = document.querySelector('.cursor');
        const cursorFollower = document.querySelector('.cursor-follower');
        const glow = document.getElementById('glow');

        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
            
            setTimeout(() => {
                cursorFollower.style.left = e.clientX + 'px';
                cursorFollower.style.top = e.clientY + 'px';
            }, 50);
            
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
        });

        // Hover effect for interactive elements
        const interactiveElements = document.querySelectorAll('button, input, .instagram-btn');
        interactiveElements.forEach(el => {
            el.addEventListener('mouseenter', () => {
                cursor.style.transform = 'scale(1.5)';
                cursorFollower.style.transform = 'scale(1.2)';
            });
            el.addEventListener('mouseleave', () => {
                cursor.style.transform = 'scale(1)';
                cursorFollower.style.transform = 'scale(1)';
            });
        });

        // Create Floating Particles
        function createParticle() {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            
            const size = Math.random() * 5 + 2;
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.left = Math.random() * 100 + 'vw';
            particle.style.animationDuration = (Math.random() * 8 + 4) + 's';
            particle.style.animationDelay = Math.random() * 5 + 's';
            particle.style.opacity = Math.random() * 0.5 + 0.3;
            
            document.body.appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, parseFloat(particle.style.animationDuration) * 1000);
        }

        // Generate initial particles
        for(let i = 0; i < 50; i++) {
            setTimeout(() => createParticle(), i * 100);
        }

        // Continuously generate particles
        setInterval(() => {
            if(document.body.children.length < 200) {
                for(let i = 0; i < 3; i++) {
                    setTimeout(() => createParticle(), i * 100);
                }
            }
        }, 1000);

        // Loading animation on form submit
        const form = document.getElementById('searchForm');
        const loading = document.getElementById('loading');
        
        if(form) {
            form.addEventListener('submit', function() {
                loading.classList.add('active');
            });
        }

        // Input validation for mobile number
        const mobileInput = document.querySelector('input[name="number"]');
        if(mobileInput) {
            mobileInput.addEventListener('input', function(e) {
                this.value = this.value.replace(/[^0-9]/g, '').slice(0, 10);
            });
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        number = request.form.get("number")
        
        if not number:
            return render_template_string(HTML, error="Please enter a mobile number.")
        
        # Validate mobile number (10 digits)
        if not number.isdigit() or len(number) != 10:
            return render_template_string(HTML, error="Please enter a valid 10-digit mobile number.")
        
        # Construct the URL
        url = f"https://ye-lo-mojkro.noob73613.workers.dev/?api_key=@noob11001&number={number}"
        
        try:
            # Make the API request
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # Extract data from the response
            message = data.get("message", "")
            query_type = data.get("query_type", "")
            query_value = data.get("query_value", "")
            total_results = data.get("total_results", 0)
            results = data.get("results", [])
            highlight = data.get("highlight", "")
            first_match = data.get("first_match", {})
            
            # Remove developer info (not displayed to user)
            # but we don't need to pop it as we're not showing raw JSON
            
            # Check if results exist
            if total_results == 0 or not results:
                return render_template_string(HTML, error="No data found for this mobile number.")
            
            return render_template_string(
                HTML, 
                message=message,
                query_type=query_type,
                query_value=query_value,
                total_results=total_results,
                results=results,
                highlight=highlight
            )
                
        except requests.exceptions.Timeout:
            return render_template_string(HTML, error="Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            return render_template_string(HTML, error="Connection error. Please check your internet connection.")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return render_template_string(HTML, error="API endpoint not found.")
            else:
                return render_template_string(HTML, error=f"HTTP Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            return render_template_string(HTML, error=f"Request failed: {str(e)}")
        except json.JSONDecodeError:
            return render_template_string(HTML, error="Invalid response from server. The response is not valid JSON.")
        except Exception as e:
            return render_template_string(HTML, error=f"An unexpected error occurred: {str(e)}")
    
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)