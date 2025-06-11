import os
from flask import Flask, request, redirect, render_template_string
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Check if environment variables are loaded
if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: Supabase credentials not found in environment variables!")
    print("Make sure you have a .env file with SUPABASE_URL and SUPABASE_KEY")
else:
    print("Supabase credentials loaded successfully")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client created successfully")
except Exception as e:
    print(f"Error creating Supabase client: {e}")
    supabase = None

# Home page template
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
          
          <form action="/submit" method="POST">
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

profile_page = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Digital Profile</title>
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
      --whatsapp-green: #25D366;
      --whatsapp-dark: #128C7E;
      --text-light: #e2e8f0;
      --glass-bg: rgba(255, 255, 255, 0.1);
      --glass-border: rgba(255, 255, 255, 0.2);
    }
    
    body {
      font-family: 'Poppins', sans-serif;
      background: linear-gradient(135deg, #0f172a, #1e293b);
      color: var(--text-light);
      min-height: 100vh;
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
    
    .profile-container {
      padding: 3rem 0;
    }
    
    .profile-header {
      text-align: center;
      margin-bottom: 3rem;
    }
    
    .profile-avatar {
      width: 150px;
      height: 150px;
      border-radius: 50%;
      object-fit: cover;
      border: 5px solid var(--primary-color);
      margin-bottom: 1.5rem;
      box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
      transition: all 0.3s ease;
    }
    
    .profile-avatar:hover {
      transform: scale(1.05);
      box-shadow: 0 15px 40px rgba(99, 102, 241, 0.4);
    }
    
    .profile-name {
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
      background: linear-gradient(90deg, #6366f1, #a855f7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    
    .profile-title {
      font-size: 1.2rem;
      color: var(--text-light);
      opacity: 0.8;
      margin-bottom: 1.5rem;
    }
    
    .glass-card {
      background: var(--glass-bg);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-radius: 16px;
      border: 1px solid var(--glass-border);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
      padding: 2rem;
      margin-bottom: 2rem;
      transition: all 0.5s ease;
    }
    
    .glass-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    .section-title {
      font-size: 1.5rem;
      font-weight: 600;
      margin-bottom: 1.5rem;
      color: var(--primary-color);
      position: relative;
      display: inline-block;
    }
    
    .section-title::after {
      content: '';
      position: absolute;
      bottom: -8px;
      left: 0;
      width: 50%;
      height: 3px;
      background: linear-gradient(90deg, #6366f1, #a855f7);
      border-radius: 3px;
    }
    
    .contact-item {
      display: flex;
      align-items: center;
      margin-bottom: 1rem;
      padding: 0.75rem;
      border-radius: 10px;
      transition: all 0.3s ease;
    }
    
    .contact-item:hover {
      background: rgba(99, 102, 241, 0.1);
      transform: translateX(5px);
    }
    
    .contact-icon {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: rgba(99, 102, 241, 0.2);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 1rem;
      color: var(--primary-color);
      font-size: 1.2rem;
    }
    
    .contact-text {
      flex: 1;
    }
    
    .contact-label {
      font-size: 0.8rem;
      color: rgba(255, 255, 255, 0.6);
      margin-bottom: 0.2rem;
    }
    
    .contact-value {
      font-size: 1rem;
      font-weight: 500;
    }
    
    .contact-value a {
      color: white;
      text-decoration: none;
      transition: all 0.3s ease;
    }
    
    .contact-value a:hover {
      color: var(--primary-color);
      text-decoration: underline;
    }
    
    .social-links {
      display: flex;
      justify-content: center;
      margin-top: 2rem;
    }
    
    .social-icon {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: var(--glass-bg);
      color: white;
      margin: 0 10px;
      font-size: 1.25rem;
      transition: all 0.3s ease;
      border: 1px solid var(--glass-border);
    }
    
    .social-icon:hover {
      background: var(--primary-color);
      transform: translateY(-5px) scale(1.1);
      color: white;
    }
    
    .floating {
      animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
      0% { transform: translateY(0px); }
      50% { transform: translateY(-15px); }
      100% { transform: translateY(0px); }
    }
    
    .divider {
      height: 3px;
      width: 80px;
      background: linear-gradient(90deg, #6366f1, #a855f7);
      margin: 1.5rem auto;
      border-radius: 3px;
    }
    
    .welcome-message {
      text-align: center;
      margin-bottom: 2rem;
      font-size: 1.1rem;
    }
    
    .welcome-name {
      font-weight: 600;
      color: var(--primary-color);
    }
  .about-section {
      margin-bottom: 3rem;
    }
    
    .detail-card {
      background: var(--glass-bg);
      backdrop-filter: blur(12px);
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 1.5rem;
      border: 1px solid var(--glass-border);
      transition: all 0.3s ease;
    }
    
    .detail-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    
    .detail-title {
      font-size: 1.2rem;
      font-weight: 600;
      margin-bottom: 1rem;
      color: var(--primary-color);
      display: flex;
      align-items: center;
    }
    
    .detail-title i {
      margin-right: 10px;
    }
    
    .skills-container {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 1rem;
    }
    
    .skill-pill {
      background: rgba(99, 102, 241, 0.2);
      color: white;
      padding: 0.5rem 1rem;
      border-radius: 20px;
      font-size: 0.9rem;
      transition: all 0.3s ease;
    }
    
    .skill-pill:hover {
      background: var(--primary-color);
      transform: scale(1.05);
    }
    
    .interests-container {
      display: flex;
      flex-wrap: wrap;
      gap: 15px;
    }
    
    .interest-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 80px;
    }
    
    .interest-icon {
      width: 50px;
      height: 50px;
      background: rgba(99, 102, 241, 0.2);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 0.5rem;
      font-size: 1.2rem;
      color: var(--primary-color);
      transition: all 0.3s ease;
    }
    
    .interest-item:hover .interest-icon {
      background: var(--primary-color);
      color: white;
      transform: scale(1.1);
    }
    
    .timeline {
      position: relative;
      padding-left: 30px;
    }
    
    .timeline::before {
      content: '';
      position: absolute;
      left: 10px;
      top: 0;
      bottom: 0;
      width: 2px;
      background: var(--primary-color);
    }
    
    .timeline-item {
      position: relative;
      margin-bottom: 1.5rem;
    }
    
    .timeline-item::before {
      content: '';
      position: absolute;
      left: -28px;
      top: 5px;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: var(--primary-color);
    }
    
    .timeline-date {
      font-size: 0.8rem;
      color: rgba(255,255,255,0.7);
    }
    
    .timeline-content {
      background: rgba(255,255,255,0.05);
      padding: 1rem;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <!-- Animated Background Particles -->
  <div class="particles" id="particles-js"></div>
  
  <div class="profile-container">
    <div class="container">
      <div class="profile-header animate__animated animate__fadeIn">
        <img src="https://res.cloudinary.com/dn4w0lvba/image/upload/v1749572617/6179377016390926731_rqzbq0.jpg" 
             alt="Profile Picture" class="profile-avatar floating">
        <h1 class="profile-name">Jesol Paul</h1>
        <p class="profile-title">Digital Creator & Developer</p>
        <div class="welcome-message">
          Welcome, <span class="welcome-name">{{ name }}</span>! Thanks for visiting my profile.
        </div>
        <div class="divider"></div>
      </div>
      <div class="profile-container">
    <div class="container">
      <!-- [Previous profile header remains the same] -->
      
      <!-- About Me Section -->
      <div class="row about-section">
        <div class="col-lg-12">
          <div class="glass-card animate__animated animate__fadeIn">
            <h2 class="section-title">About Me</h2>
            <p>Hello! I'm Jesol Paul, a passionate developer and digital marketer based in Ernakulam, India. 
            I love creating innovative solutions and exploring new technologies. When I'm not coding, you can 
            find me playing chess or learning new marketing strategies.</p>
          </div>
        </div>
      </div>
      
      <div class="row">
        <!-- Left Column -->
        <div class="col-lg-6">
          <!-- [Previous contact information remains the same] -->
          
          <!-- Education -->
          <div class="detail-card animate__animated animate__fadeInLeft">
            <h3 class="detail-title"><i class="fas fa-graduation-cap"></i> Education</h3>
            <div class="timeline">
              <div class="timeline-item">
                <div class="timeline-date">2020 - 2023</div>
                <div class="timeline-content">
                  <h5>Bachelor of Computer Applications (BCA)</h5>
                  <p>Completed with honors from MG University, Kerala</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Location -->
          <div class="detail-card animate__animated animate__fadeInLeft">
            <h3 class="detail-title"><i class="fas fa-map-marker-alt"></i> Location</h3>
            <p><i class="fas fa-city"></i> Ernakulam, Kerala, India</p>
            <div id="map" style="height: 200px; width: 100%; border-radius: 8px; margin-top: 1rem; background: rgba(255,255,255,0.1);"></div>
          </div>
        </div>
        
        <!-- Right Column -->
        <div class="col-lg-6">
          <!-- Technical Skills -->
          <div class="detail-card animate__animated animate__fadeInRight">
            <h3 class="detail-title"><i class="fas fa-code"></i> Technical Skills</h3>
            <div class="skills-container">
              <span class="skill-pill">C</span>
              <span class="skill-pill">C++</span>
              <span class="skill-pill">Python</span>
              <span class="skill-pill">Java</span>
              <span class="skill-pill">Django</span>
              <span class="skill-pill">PHP</span>
              <span class="skill-pill">HTML/CSS</span>
              <span class="skill-pill">JavaScript</span>
              <span class="skill-pill">SQL</span>
              <span class="skill-pill">Flask</span>
              <span class="skill-pill">Git</span>
            </div>
          </div>
          
          <!-- Interests -->
          <div class="detail-card animate__animated animate__fadeInRight">
            <h3 class="detail-title"><i class="fas fa-heart"></i> Interests</h3>
            <div class="interests-container">
              <div class="interest-item">
                <div class="interest-icon">
                  <i class="fas fa-chess"></i>
                </div>
                <span>Chess</span>
              </div>
              <div class="interest-item">
                <div class="interest-icon">
                  <i class="fas fa-chart-line"></i>
                </div>
                <span>Digital Marketing</span>
              </div>
              <div class="interest-item">
                <div class="interest-icon">
                  <i class="fas fa-music"></i>
                </div>
                <span>Music</span>
              </div>
              <div class="interest-item">
                <div class="interest-icon">
                  <i class="fas fa-book"></i>
                </div>
                <span>Reading</span>
              </div>
            </div>
          </div>
          
          <!-- Digital Marketing -->
          <div class="detail-card animate__animated animate__fadeInRight">
            <h3 class="detail-title"><i class="fas fa-bullhorn"></i> Digital Marketing</h3>
            <p>Experienced in SEO, Social Media Marketing, and Content Strategy with proven results in increasing online presence and engagement.</p>
            <div class="skills-container" style="margin-top: 1rem;">
              <span class="skill-pill">SEO</span>
              <span class="skill-pill">Social Media</span>
              <span class="skill-pill">Content Strategy</span>
              <span class="skill-pill">Google Analytics</span>
              <span class="skill-pill">Ads</span>
            </div>
          </div>
        </div>
      </div>
      
      
      <div class="row">
        <div class="col-lg-6">
          <div class="glass-card animate__animated animate__fadeInLeft">
            <h2 class="section-title">Contact Information</h2>
            
            <div class="contact-item">
              <div class="contact-icon">
                <i class="fas fa-envelope"></i>
              </div>
              <div class="contact-text">
                <div class="contact-label">Email</div>
                <div class="contact-value">jesolpaul@gmail.com</div>
              </div>
            </div>
            
            <div class="contact-item">
              <div class="contact-icon">
                <i class="fas fa-phone"></i>
              </div>
              <div class="contact-text">
                <div class="contact-label">Phone</div>
                <div class="contact-value">+91 7994422545</div>
              </div>
            </div>
            
            <div class="contact-item whatsapp-item">
              <div class="contact-icon whatsapp-icon">
                <i class="fab fa-whatsapp"></i>
              </div>
              <div class="contact-text">
                <div class="contact-label">WhatsApp</div>
                <div class="contact-value">
                  <a href="https://wa.me/917994422545" target="_blank">+91 7994422545</a>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-lg-6">
          <div class="glass-card animate__animated animate__fadeInRight">
            <h2 class="section-title">Social Profiles</h2>
            
            <div class="contact-item">
              <div class="contact-icon">
                <i class="fab fa-telegram"></i>
              </div>
              <div class="contact-text">
                <div class="contact-label">Telegram</div>
                <div class="contact-value">
                  <a href="https://t.me/jesolizm" target="_blank">@jesolizm</a>
                </div>
              </div>
            </div>
            
            <div class="contact-item">
              <div class="contact-icon">
                <i class="fab fa-linkedin"></i>
              </div>
              <div class="contact-text">
                <div class="contact-label">LinkedIn</div>
                <div class="contact-value">
                  <a href="https://www.linkedin.com/in/jesol-paul-761387317/" target="_blank">jesol-paul</a>
                </div>
              </div>
            </div>
            
            <div class="contact-item">
              <div class="contact-icon">
                <i class="fab fa-instagram"></i>
              </div>
              <div class="contact-text">
                <div class="contact-label">Instagram</div>
                <div class="contact-value">
                  <a href="https://www.instagram.com/just_jesol" target="_blank">@just_jesol</a>
                </div>
              </div>
            </div>
            
            <div class="contact-item">
              <div class="contact-icon">
                <i class="fab fa-facebook"></i>
              </div>
              <div class="contact-text">
                <div class="contact-label">Facebook</div>
                <div class="contact-value">
                  <a href="https://www.linkedin.com/in/jesol-paul-761387317/" target="_blank">jesol-paul</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="social-links">
        <a href="https://t.me/jesolizm" class="social-icon" target="_blank">
          <i class="fab fa-telegram"></i>
        </a>
        <a href="https://www.linkedin.com/in/jesol-paul-761387317/" class="social-icon" target="_blank">
          <i class="fab fa-linkedin"></i>
        </a>
        <a href="https://www.instagram.com/just_jesol" class="social-icon" target="_blank">
          <i class="fab fa-instagram"></i>
        </a>
        <a href="https://www.linkedin.com/in/jesol-paul-761387317/" class="social-icon" target="_blank">
          <i class="fab fa-facebook"></i>
        </a>
        <a href="https://wa.me/917994422545" class="social-icon whatsapp-btn" target="_blank">
          <i class="fab fa-whatsapp"></i>
        </a>
      </div>
      
      <!-- WhatsApp Floating Button -->
      <div class="position-fixed bottom-0 end-0 m-4">
        <a href="https://wa.me/917994422545" class="btn btn-success btn-lg rounded-pill shadow-lg whatsapp-btn pulse" target="_blank">
          <i class="fab fa-whatsapp me-2"></i> Chat on WhatsApp
        </a>
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
 <!-- Add Leaflet.js for map -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
  <script>
    // Initialize map (Ernakulam, India)
    document.addEventListener('DOMContentLoaded', function() {
      const map = L.map('map').setView([9.9816, 76.2999], 12);
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);
      
      L.marker([9.9816, 76.2999]).addTo(map)
        .bindPopup('Ernakulam, Kerala, India')
        .openPopup();
    });
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(home_page)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    if not name:
        return "Please enter your name.", 400

    try:
        # Insert the name into the "visitors" table in Supabase
        response = supabase.table("visitors").insert({"name": name}).execute()
        
        if response.data:
            print("Successfully stored name:", name)
            # Render profile page with the visitor's name
            return render_template_string(profile_page.replace("{{ name }}", name))
        else:
            print("Failed to store name. Response:", response)
            return "Error saving your name. Please try again.", 500
            
    except Exception as e:
        print("Error saving your name:", e)
        return "Error processing your request. Please try again.", 500

if __name__ == "__main__":
    app.run(port=3000, debug=True)
