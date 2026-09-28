"""
Root terminal entrypoint for Savitha Canteen Food Demand Prediction & Campus Dining System.
Allows running directly from your terminal:
    python run.py
    python app.py
    python main.py
"""
import os
import sys
import argparse

# Ensure project root is in sys.path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

def check_dependencies():
    """Verify required Python packages are installed before starting."""
    missing = []
    packages = [
        ("flask", "Flask"),
        ("flask_cors", "flask-cors"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("sklearn", "scikit-learn"),
        ("joblib", "joblib")
    ]
    for module_name, pip_name in packages:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(pip_name)
    
    if missing:
        print("=" * 70)
        print(" [!] Missing Required Dependencies")
        print("=" * 70)
        print(" The following Python packages need to be installed:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n Run the following command in your terminal to install them:")
        print(f"   pip install -r requirements.txt")
        print("=" * 70)
        sys.exit(1)

def main():
    check_dependencies()

    parser = argparse.ArgumentParser(description="Savitha Canteen Food Demand & Ordering Server")
    parser.add_argument("--port", type=int, default=5000, help="Port to run server on (default: 5000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host IP to bind to (default: 0.0.0.0)")
    args = parser.parse_args()

    from backend.app import app, run_server
    run_server(port=args.port, host=args.host)

if __name__ == "__main__":
    main()
