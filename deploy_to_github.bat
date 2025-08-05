@echo off
echo.
echo ========================================
echo   SIMS - GitHub Deployment Helper
echo   by Mustapha Baroudi
echo ========================================
echo.

echo Preparing files for deployment...
echo.

REM Create deployment package
echo Creating deployment files...
copy app_deploy.py app.py
copy requirements_deploy.txt requirements.txt

echo.
echo Files ready for GitHub upload:
echo - app_deploy.py (main Flask application)
echo - requirements_deploy.txt (dependencies)
echo - Procfile (deployment config)
echo - runtime.txt (Python version)
echo - vercel.json (Vercel config)
echo - app.yaml (Google App Engine config)
echo.

echo ========================================
echo   NEXT STEPS:
echo ========================================
echo.
echo 1. Go to github.com and create new repository
echo 2. Name it: sims-inventory-mustapha-baroudi
echo 3. Upload all files from this folder
echo 4. Go to render.com or railway.app
echo 5. Connect your GitHub repository
echo 6. Deploy automatically!
echo.
echo Your app will be live in 5 minutes!
echo.
echo ========================================
echo   CONTACT MUSTAPHA BAROUDI:
echo ========================================
echo Phone: +212 697 362 759
echo Email: mustaphabaroudi833@gmail.com
echo LinkedIn: linkedin.com/in/baroudi-mustapha-2a257a289/
echo.

pause
