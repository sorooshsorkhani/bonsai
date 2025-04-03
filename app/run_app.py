import os
import sys

# Add the 'app' directory to the Python path dynamically
app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
if app_path not in sys.path:
    sys.path.append(app_path)

# Now, we can safely import the frontend UI script
if __name__ == "__main__":
    os.system("streamlit run app/frontend/ui.py")
