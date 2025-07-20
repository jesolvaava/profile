import os
from flask import Flask, request, render_template_string
from supabase import create_client, Client

# Initialize the Flask app
app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = None
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client created successfully.")
except Exception as e:
    print("Error creating Supabase client:", e)
    supabase = None

# Home page HTML
home_page = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome to My Profile</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root { --primary-color: #6366f1; --primary-dark: #4f46e5; --text-light: #e2e8f0; --glass-bg: rgba(255, 255, 255, 0.1); --glass-border: rgba(255, 255, 255, 0.2);}
    body { font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #0f172a, #1e293b); color: var(--text-light); min-height: 100vh; }
    .glass-card { background: var(--glass-bg); backdrop-filter: blur(12px); border-radius: 16px; border: 1px solid var(--glass-border); box-shadow: 0 8px 32px rgba(0,0,0,0.3); padding: 2.5rem; transition: all 0.5s ease;}
    .glass-card:hover { transform: translateY(-10px); box-shadow: 0 12px 40px rgba(0,0,0,0.4);}
    .form-control { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; padding: 0.75rem 1.25rem; border-radius: 12px; }
    .form-control:focus { background: rgba(255,255,255,0.15); border-color: var(--primary-color); color: white;}
    .btn-primary { background: var(--primary-color); border: none; padding: 0.75rem 1.5rem; border-radius: 12px; font-weight: 500; transition: all 0.3s ease;}
    .btn-primary:hover { background: var(--primary-dark);}
    .title { font-weight: 700; background: linear-gradient(90deg, #6366f1, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1.5rem;}
    .divider { height: 3px; width: 80px; background: linear-gradient(90deg, #6366f1, #a855f7); margin: 1.5rem auto; border-radius: 3px;}
  </style>
</head>
<body>
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
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# Profile page HTML
profile_page = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Digital Profile</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root { --primary-color: #6366f1; --primary-dark: #4f46e5; --text-light: #e2e8f0; --glass-bg: rgba(255,255,255,0.1); --glass-border: rgba(255,255,255,0.2);}
    body { font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #0f172a, #1e293b); color: var(--text-light); min-height: 100vh; }
    .profile-header { text-align: center; margin-bottom: 3rem; }
    .profile-avatar { width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 5px solid var(--primary-color); margin-bottom: 1.5rem; box-shadow: 0 10px 30px rgba(99,102,241,0.3);}
    .profile-name { font-size: 2.5rem; font-weight: 700; background: linear-gradient(90deg, #6366f1, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .welcome-message { text-align: center; margin-bottom: 2rem; font-size: 1.1rem;}
    .welcome-name { font-weight: 600; color: var(--primary-color); }
    .glass-card { background: var(--glass-bg); backdrop-filter: blur(12px); border-radius: 16px; border: 1px solid var(--glass-border); box-shadow: 0 8px 32px rgba(0,0,0,0.3); padding: 2rem; margin-bottom: 2rem;}
    .section-title { font-size: 1.5rem; font-weight: 600; margin-bottom: 1.5rem; color: var(--primary-color);}
    .contact-item { display: flex; align-items: center; margin-bottom: 1rem; padding: 0.75rem; border-radius: 10px; }
    .contact-icon { width: 40px; height: 40px; border-radius: 50%; background: rgba(99,102,241,0.2); display: flex; align-items: center; justify-content: center; margin-right: 1rem; color: var(--primary-color);}
    .contact-label { font-size: 0.8rem; color: rgba(255,255,255,0.6);}
    .contact-value { font-size: 1rem; font-weight: 500;}
    .contact-value a { color: white; text-decoration: none;}
    .contact-value a:hover { color: var(--primary-color);}
    .skills-container { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 1rem;}
    .skill-pill { background: rgba(99,102,241,0.2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;}
    .divider { height: 3px; width: 80px; background: linear-gradient(90deg, #6366f1, #a855f7); margin: 1.5rem auto; border-radius: 3px;}
  </style>
</head>
<body>
  <div class="container py-5">
    <div class="profile-header animate__animated animate__fadeIn">
      <img src="https://res.cloudinary.com/dn4w0lvba/image/upload/v1749621716/6310049777169057704_qhatih.jpg" alt="Profile Picture" class="profile-avatar floating">
      <h1 class="profile-name">Jesol Paul</h1>
      <p class="profile-title">Digital Creator & Developer</p>
      <div class="welcome-message">
        Welcome, <span class="welcome-name">{{ name }}</span>! Thanks for visiting my profile.
      </div>
      <div class="divider"></div>
    </div>
    <div class="row">
      <div class="col-lg-6 mb-4">
        <div class="glass-card animate__animated animate__fadeInLeft">
          <h2 class="section-title">About Me</h2>
          <p>Hello! I'm Jesol Paul, a passionate developer and digital marketer based in Ernakulam, India. 
          I love creating innovative solutions and exploring new technologies. When I'm not coding, you can 
          find me playing chess or learning new marketing strategies.</p>
        </div>
        <div class="glass-card animate__animated animate__fadeInLeft">
          <h3 class="section-title">Education</h3>
          <div><strong>2022 - 2025</strong>: Bachelor of Computer Applications (BCA), MG University, Kerala</div>
        </div>
        <div class="glass-card animate__animated animate__fadeInLeft">
          <h3 class="section-title">Location</h3>
          <p><i class="fas fa-map-marker-alt"></i> KL44, Ernakulam, Kerala, India</p>
        </div>
      </div>
      <div class="col-lg-6 mb-4">
        <div class="glass-card animate__animated animate__fadeInRight">
          <h3 class="section-title">Technical Skills</h3>
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
        <div class="glass-card animate__animated animate__fadeInRight">
          <h3 class="section-title">Interests</h3>
          <div class="skills-container">
            <span class="skill-pill">Chess</span>
            <span class="skill-pill">Digital Marketing</span>
            <span class="skill-pill">Music</span>
            <span class="skill-pill">Reading</span>
          </div>
        </div>
        <div class="glass-card animate__animated animate__fadeInRight">
          <h3 class="section-title">Digital Marketing</h3>
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
      <div class="col-lg-6 mb-4">
        <div class="glass-card animate__animated animate__fadeInLeft">
          <h2 class="section-title">Contact Information</h2>
          <div class="contact-item">
            <div class="contact-icon"><i class="fas fa-envelope"></i></div>
            <div>
              <div class="contact-label">Email</div>
              <div class="contact-value">jesolpaul@gmail.com</div>
            </div>
          </div>
          <div class="contact-item">
            <div class="contact-icon"><i class="fas fa-phone"></i></div>
            <div>
              <div class="contact-label">Phone</div>
              <div class="contact-value">+91 7994422545</div>
            </div>
          </div>
          <div class="contact-item whatsapp-item">
            <div class="contact-icon whatsapp-icon"><i class="fab fa-whatsapp"></i></div>
            <div>
              <div class="contact-label">WhatsApp</div>
              <div class="contact-value"><a href="https://wa.me/917994422545" target="_blank">+91 7994422545</a></div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-6 mb-4">
        <div class="glass-card animate__animated animate__fadeInRight">
          <h2 class="section-title">Social Profiles</h2>
          <div class="contact-item">
            <div class="contact-icon"><i class="fab fa-telegram"></i></div>
            <div>
              <div class="contact-label">Telegram</div>
              <div class="contact-value"><a href="https://t.me/jesolizm" target="_blank">@jesolizm</a></div>
            </div>
          </div>
          <div class="contact-item">
            <div class="contact-icon"><i class="fab fa-linkedin"></i></div>
            <div>
              <div class="contact-label">LinkedIn</div>
              <div class="contact-value"><a href="https://www.linkedin.com/in/jesol-paul-761387317/" target="_blank">jesol-paul</a></div>
            </div>
          </div>
          <div class="contact-item">
            <div class="contact-icon"><i class="fab fa-instagram"></i></div>
            <div>
              <div class="contact-label">Instagram</div>
              <div class="contact-value"><a href="https://www.instagram.com/just_jesol" target="_blank">@just_jesol</a></div>
            </div>
          </div>
          <div class="contact-item">
            <div class="contact-icon"><i class="fab fa-facebook"></i></div>
            <div>
              <div class="contact-label">Facebook</div>
              <div class="contact-value"><a href="https://www.linkedin.com/in/jesol-paul-761387317/" target="_blank">jesol-paul</a></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="my-4 mb-5 d-flex justify-content-center">
      <a href="https://t.me/jesolizm" class="btn btn-outline-primary mx-2" target="_blank"><i class="fab fa-telegram"></i></a>
      <a href="https://www.linkedin.com/in/jesol-paul-761387317/" class="btn btn-outline-primary mx-2" target="_blank"><i class="fab fa-linkedin"></i></a>
      <a href="https://www.instagram.com/just_jesol" class="btn btn-outline-primary mx-2" target="_blank"><i class="fab fa-instagram"></i></a>
      <a href="https://wa.me/917994422545" class="btn btn-success mx-2" target="_blank"><i class="fab fa-whatsapp"></i></a>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(home_page)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    if not name:
        return "Please enter your name.", 400
    if not supabase:
        return "Server configuration error (database not connected).", 500
    try:
        response = supabase.table("visitors").insert({"name": name}).execute()
        if response.data:
            return render_template_string(profile_page.replace("{{ name }}", name))
        else:
            print("Failed to store name. Response:", response)
            return "Error saving your name. Please try again.", 500
    except Exception as e:
        print("Error saving your name:", e)
        return "Error processing your request. Please try again.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
