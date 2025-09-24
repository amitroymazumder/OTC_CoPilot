import os
import subprocess

def main():
    print("🚀 Starting OTC Ops Copilot...")

    # Launch Streamlit UI
    os.environ["STREAMLIT_ENV"] = "production"
    subprocess.run(["streamlit", "run", "app/app.py"])

if __name__ == "__main__":
    main()
