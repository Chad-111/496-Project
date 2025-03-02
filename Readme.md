# [DraftEmpire](https://draftempire.win "Draft Empire Website") [CS 496 Semester Project]

# Project Structure
```bash
496-Project/
│-- frontend/  # React frontend
│   │-- src/   # Source code for the React app
│   │-- public/ # Static assets (HTML, icons, etc.)
│   │-- package.json  # Dependencies & scripts
│-- backend/   # (If applicable) Backend server
│-- docs/      # Documentation & project guidelines
│-- README.md  # This document
```
_________________

## Setting Up the Project <mark>(Local Environment)</mark>

### 1. Clone the Repo
First, clone the project to your local machine:
```bash
cd C:\Projects  # Change to a directory where you want to store the project
git clone https://github.com/Chad-111/496-Project.git
cd 496-Project
```
### 2. Install Dependencies
For the frontend, navigate to the `frontend` folder and install required packages
```bash
cd frontend
npm install
```
For the backend, install its dependencies as well
```bash
cd ../backend
pip install -r requirements.txt
```
_________________

## Creating a New Feature or Making Changes

### 1. Create a New Branch
**Always work on a new branch instead of `master`**
```bash
git checkout -b branch-name # Replace <branch-name> with whatever you want
```
### 2. Make Changes
Modify the necessary files in the `frontend/` or `backend/` directory </br>
> **React** <mark>*Frontend*</mark>
```bash
cd frontend
npm start # Runs the app locally for testing
```
> **Flask (Python)** <mark>*Backend*</mark>
```bash
cd backend
python app.py # Runs the backend server
```
### 3. Commit & Push Changes
After making changes, commit and push your branch to `master`
```bash
git add .
git commit -m "Added new feature"
git push origin branch-name # Replace <branch-name> with what you named it in Step #1
```
### 4. Create a Pull Request (PR)
1. Goto GitHub -> 496-Project
2. Navigate to the `Pull Requests` tab
3. Click `New Pull Request` and select your branch you created in Step #1
4. Add a description of your changes, similarly to the previous step ("Added new feature")
5. Request a review
6. After approval, it will be merged into `master`
_________________

## What Happens After a Commit?
Once your PR is merged, the latest version is automatically pulled into the server via WebHook </br>
The frontend is rebuilt, and the backend is restarted </br>
Changes go live instantly! </br>
