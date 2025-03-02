# What is a Webhook?
A webhook is an automated system that listens for events (such as a commit) and triggers specific actions on our server.

# How Our Webhook is Set Up

### GitHub Webhook:
Configured in GitHub to send POST requests to our server whenever a commit is pushed. <br>
The webhook URL is dynamically updated via Ngrok to ensure GitHub can always reach our machine.<br>

### Ngrok Tunnel:
Since we host the server locally (on my PC), Ngrok exposes our webhook listener to the internet with a secure public URL. <br>
The webhook dynamically updates its URL in GitHub whenever Ngrok restarts.<br>

### Python Webhook Listener:
Runs on our machine and listens for GitHub webhook events. <br>
When a push is detected on the master branch, it triggers our deployment script. <br>
Functions inside script:
> `def get_ngrok_url():`
> - **Fetch the current Ngrok public URL**

> `def update_github_webhook():`
> - **Update GitHub Webhook to use the latest Ngrok URL**

### Deployment Script (`update_project.bat`)
Automatically pulls the latest code. <br>
Installs new dependencies if needed. <br>
Builds the frontend and deploys it to the Apache server. <br>
Restarts Apache to serve the updated version. <br>

# What Happens After a Commit?
You push a commit to GitHub. <br>
GitHub sends a webhook request to our server via Ngrok. <br>
The webhook listener runs update_project.bat to pull the latest changes and rebuild the project. <br>
The changes go live instantly! <br>
