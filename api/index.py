import os
from flask import Flask, request, redirect, render_template_string
from supabase import create_client, Client

app = Flask(__name__)

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Check if environment variables are loaded
if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: Supabase credentials not found in environment variables!")
else:
    print("Supabase credentials loaded successfully")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client created successfully")
except Exception as e:
    print(f"Error creating Supabase client: {e}")
    supabase = None

# [Your existing HTML templates remain the same - home_page and profile_page]
home_page = """
<!-- Your existing home_page HTML content -->
"""

profile_page = """
<!-- Your existing profile_page HTML content -->
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

# This is important for Vercel
if __name__ == "__main__":
    app.run()
