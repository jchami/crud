import os
# PRODUCTION
from app import app

if __name__ == "__main__":
    # DEVELOPMENT
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000), debug=True)
