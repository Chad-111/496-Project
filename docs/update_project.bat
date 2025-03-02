@echo off
cd C:\DraftEmpire\496-Project
echo Pulling latest changes...
git pull origin master

echo Installing dependencies...
cd frontend
call npm install

echo Building project...
call npm run build

echo Deploying build to Apache...
xcopy /E /I /Y /Q "C:\DraftEmpire\496-Project\frontend\dist" "C:\Apache24\htdocs"

echo Restarting Apache...
httpd.exe -k restart

echo Update complete!
