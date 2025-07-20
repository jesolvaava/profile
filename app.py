import os
from flask import Flask, request, redirect, render_template_string
from supabase import create_client, Client

# Environment variables are expected to be set
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Early error check, but do NOT crash the import (function will error, logs visible in Vercel)
if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: Supabase credentials not found in environment variables!")
    print("Set SUPABASE_URL and SUPABASE_KEY in Vercel dashboard.")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Error creating Supabase client: {e}")
    supabase = None

app = Flask(__name__)

# [Snip: Define home_page and profile_page template strings - copy as-is from your code above]
home_page = """ ... """  # use your HTML code for home_page
profile_page = """ ... """ # use your HTML code for profile_page

@app.route("/", methods=["GET"])
def home():
    return render_template_string(home_page)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    if not name:
        return "Please enter your name.", 400
    if not supabase:
        print("Supabase client is not available!")
        return "Server configuration error. Please contact the admin.", 500

    try:
        response = supabase.table("visitors").insert({"name": name}).execute()
        if response and getattr(response, "data", None):
            print("Successfully stored name:", name)
            return render_template_string(profile_page.replace("{{ name }}", name))
        else:
            print("Failed to store name. Response:", response)
            return "Error saving your name. Please try again.", 500

    except Exception as e:
        print("Error saving your name:", e)
        return "Error processing your request. Please try again.", 500

# No app.run()! Vercel manages the webserver. Do NOT include this:
# if __name__ == "__main__":
#     app.run(port=3000, debug=True)

# For Vercel compatibility
app = app  # Vercel looks for this 'app' object


