"""
Run script for the dashboard
"""
from app import app, init_db
from pathlib import Path

if __name__ == '__main__':
    # Create necessary directories
    Path('uploads').mkdir(exist_ok=True)
    Path('uploads/logs').mkdir(exist_ok=True)
    Path('uploads/videos').mkdir(exist_ok=True)
    Path('uploads/network').mkdir(exist_ok=True)
    
    # Initialize database
    init_db()
    
    print("\n" + "="*60)
    print("Cybersecurity Dashboard Starting...")
    print("="*60)
    print("Access at: http://localhost:5000")
    print("Default login: admin / admin123")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)


