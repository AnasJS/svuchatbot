from src.svuchatbot_api.api import app
@app.route("/")
def get_message():
    return "<p>Hello, World!</p>"