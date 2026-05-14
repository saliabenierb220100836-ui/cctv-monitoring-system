import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Railway provides the port via an environment variable named 'PORT'
    # We convert it to an integer, or default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    
    # host='0.0.0.0' is mandatory so the container can accept external traffic
    app.run(host='0.0.0.0', port=port)