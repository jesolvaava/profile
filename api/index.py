from flask import Flask, request, render_template_string
from supabase import create_client, Client
import os

# Initialize Flask app
app = Flask(__name__)

# Supabase configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize Supabase client
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error creating Supabase client: {e}")

# Your HTML templates (keep these exactly as they are)
home_page = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome to My Profile</title>
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <!-- Animate.css -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary-color: #6366f1;
      --primary-dark: #4f46e5;
      --text-light: #e2e8f0;
      --glass-bg: rgba(255, 255, 255, 0.1);
      --glass-border: rgba(255, 255, 255, 0.2);
    }
    
    body {
      font-family: 'Poppins', sans-serif;
      background: linear-gradient(135deg, #0f172a, #1e293b);
      color: var(--text-light);
      min-height: 100vh;
      overflow-x: hidden;
      margin: 0;
      padding: 0;
    }
    
    .particles {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: -1;
    }
    
    .glass-card {
      background: var(--glass-bg);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-radius: 16px;
      border: 1px solid var(--glass-border);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
      padding: 2.5rem;
      transition: all 0.5s ease;
    }
    
    .glass-card:hover {
      transform: translateY(-10px);
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    .form-control {
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: white;
      padding: 0.75rem 1.25rem;
      border-radius: 12px;
      transition: all 0.3s ease;
    }
    
    .form-control:focus {
      background: rgba(255, 255, 255, 0.15);
      border-color: var(--primary-color);
      box-shadow: 0 0 0 0.25rem rgba(99, 102, 241, 0.25);
      color: white;
    }
    
    .btn-primary {
      background: var(--primary-color);
      border: none;
      padding: 0.75rem 1.5rem;
      border-radius: 12px;
      font-weight: 500;
      letter-spacing: 0.5px;
      transition: all 0.3s ease;
      position: relative;
      overflow: hidden;
    }
    
    .btn-primary:hover {
      background: var(--primary-dark);
      transform: translateY(-3px);
    }
    
    .title {
      font-weight: 700;
      background: linear-gradient(90deg, #6366f1, #a855f7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 1.5rem;
    }
    
    .floating {
      animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
      0% { transform: translateY(0px); }
      50% { transform: translateY(-15px); }
      100% { transform: translateY(0px); }
    }
    
    .pulse {
      animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
      0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.7); }
      70% { box-shadow: 0 0 0 15px rgba(99, 102, 241, 0); }
      100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
    }
    
    .divider {
      height: 3px;
      width: 80px;
      background: linear-gradient(90deg, #6366f1, #a855f7);
      margin: 1.5rem auto;
      border-radius: 3px;
    }
  </style>
</head>
<body>
  <!-- Animated Background Particles -->
  <div class="particles" id="particles-js"></div>
  
  <div class="container py-5">
    <div class="row justify-content-center align-items-center min-vh-100">
      <div class="col-lg-6 col-md-8">
        <div class="glass-card animate__animated animate__fadeIn">
          <div class="text-center mb-4">
            <i class="fas fa-user-circle feature-icon floating"></i>
            <h1 class="title display-4">Welcome</h1>
            <p class="mb-4">Enter your name to view my profile</p>
            <div class="divider"></div>
          </div>
          
          <form action="/api/submit" method="POST">
            <div class="mb-4">
              <div class="input-group">
                <span class="input-group-text bg-transparent text-white border-end-0">
                  <i class="fas fa-user"></i>
                </span>
                <input type="text" name="name" class="form-control border-start-0" placeholder="Your Name" required>
              </div>
            </div>
            
            <div class="d-grid">
              <button type="submit" class="btn btn-primary btn-lg pulse">
                Continue <i class="fas fa-arrow-right ms-2"></i>
              </button>
            </div>
          </form>
          
          <div class="text-center mt-4">
            <p class="small">By continuing, you agree to our Terms of Service</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Bootstrap JS Bundle with Popper -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  <!-- Particles.js -->
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    // Initialize particles.js
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 80,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": "#6366f1"
        },
        "shape": {
          "type": "circle",
          "stroke": {
            "width": 0,
            "color": "#000000"
          },
          "polygon": {
            "nb_sides": 5
          }
        },
        "opacity": {
          "value": 0.5,
          "random": false,
          "anim": {
            "enable": false,
            "speed": 1,
            "opacity_min": 0.1,
            "sync": false
          }
        },
        "size": {
          "value": 3,
          "random": true,
          "anim": {
            "enable": false,
            "speed": 40,
            "size_min": 0.1,
            "sync": false
          }
        },
        "line_linked": {
          "enable": true,
          "distance": 150,
          "color": "#6366f1",
          "opacity": 0.4,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 2,
          "direction": "none",
          "random": false,
          "straight": false,
          "out_mode": "out",
          "bounce": false,
          "attract": {
            "enable": false,
            "rotateX": 600,
            "rotateY": 1200
          }
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": true,
            "mode": "grab"
          },
          "onclick": {
            "enable": true,
            "mode": "push"
          },
          "resize": true
        },
        "modes": {
          "grab": {
            "distance": 140,
            "line_linked": {
              "opacity": 1
            }
          },
          "bubble": {
            "distance": 400,
            "size": 40,
            "duration": 2,
            "opacity": 8,
            "speed": 3
          },
          "repulse": {
            "distance": 200,
            "duration": 0.4
          },
          "push": {
            "particles_nb": 4
          },
          "remove": {
            "particles_nb": 2
          }
        }
      },
      "retina_detect": true
    });
  </script>
</body>
</html>
"""

# Simplified profile_page for testing - you can expand this later
profile_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Profile - {name}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome, {name}!</h1>
        <p>Thank you for visiting my profile.</p>
        <h2>Jesol Paul</h2>
        <p>Digital Creator & Developer</p>
        <p>Email: jesolpaul@gmail.com</p>
        <p>Phone: +91 7994422545</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(home_page)

@app.route('/api/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '').strip()
    if not name:
        return "Please enter your name.", 400
    
    # Try to save to Supabase if available
    if supabase:
        try:
            response = supabase.table("visitors").insert({"name": name}).execute()
            print(f"Successfully stored name: {name}")
        except Exception as e:
            print(f"Error saving to Supabase: {e}")
    
    # Return profile page with name
    return render_template_string(profile_page.format(name=name))

# Test route to verify the app is working
@app.route('/test')
def test():
    return "Flask app is working on Vercel!"

# This is crucial for Vercel
handler = app.wsgi_app
