from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import json
import requests
import time

# GitHub Webhook URL - Replace with your actual repository webhook ID
GITHUB_WEBHOOK_URL = "https://api.github.com/repos/Chad-111/496-Project/hooks/533020704"
GITHUB_TOKEN = "GITHUB_WEBHOOK_TOKEN"  # Create a GitHub token with webhook access

def get_ngrok_url():
    """Fetch the current Ngrok public URL"""
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        data = response.json()
        return data['tunnels'][0]['public_url']  # Get the first public URL
    except Exception as e:
        print(f"Error fetching Ngrok URL: {e}")
        return None

def update_github_webhook():
    """Update GitHub Webhook to use the latest Ngrok URL"""
    ngrok_url = get_ngrok_url()
    if not ngrok_url:
        print("Failed to get Ngrok URL. Webhook update skipped.")
        return
    
    webhook_data = {
        "config": {
            "url": f"{ngrok_url}/github-webhook/",
            "content_type": "json",
            "insecure_ssl": "0"
        }
    }

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.patch(GITHUB_WEBHOOK_URL, headers=headers, json=webhook_data)
    
    if response.status_code == 200:
        print(f"✅ GitHub Webhook updated to: {ngrok_url}/github-webhook/")
    else:
        print(f"❌ Failed to update webhook: {response.text}")

# Automatically update the webhook when the script starts
time.sleep(5)  # Wait a few seconds for Ngrok to initialize
update_github_webhook()

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests for debugging."""
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"GitHub Webhook Listener is running!")

    def do_POST(self):
        """Handle GitHub Webhook POST requests."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data.decode('utf-8'))
        
        if 'ref' in payload and payload['ref'] == 'refs/heads/master':  # Adjust branch if needed
            print("✅ GitHub webhook received! Pulling latest changes...")
            subprocess.run(["C:\\DraftEmpire\\496-Project\\update_project.bat"], shell=True)
        
        self.send_response(200)
        self.end_headers()

def run(server_class=HTTPServer, handler_class=WebhookHandler, port=9000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Webhook listener running on port {port}")
    httpd.serve_forever()

run()
