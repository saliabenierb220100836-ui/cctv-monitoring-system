import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Pull the dynamic port from Railway
    port = int(os.environ.get("PORT", 5000))
    # Must bind to 0.0.0.0 for the cloud to route traffic
    app.run(host="0.0.0.0", port=port)