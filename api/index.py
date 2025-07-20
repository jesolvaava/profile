import os
from flask import Flask, request, render_template_string
from supabase import create_client, Client

app = Flask(__name__)

# Setup Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error creating Supabase client: {e}")

# ---- FULL HTML Pages ----

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
  <style> /* your style as before */ </style>
</head>
<body>
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
          <form action="/" method="POST">
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
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    // ... your particles.js code ...
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
  <!-- ... all your existing <head> content ... -->
</head>
<body>
  <div class="particles" id="particles-js"></div>
  <div class="profile-container">
    <!-- ... all your profile HTML ... -->
    <div class="welcome-message">
      Welcome, <span class="welcome-name">{{ name }}</span>! Thanks for visiting my profile.
    </div>
    <!-- ... rest of your profile ... -->
  </div>
  <script src="..."></script>
  <script>
    // ... your particles.js code and leaflet.js code for map ...
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            return "Please enter your name.", 400
        # Try saving visitor's name to Supabase, but don't break UI if error
        if supabase:
            try:
                supabase.table("visitors").insert({"name": name}).execute()
            except Exception as e:
                print(f"Error saving to Supabase: {e}")
        # Render the profile page with the visitor's name
        return render_template_string(profile_page, name=name)
    # GET method: Home page
    return render_template_string(home_page)

# For Vercel, this is the entry (do NOT call app.run)
handler = app

