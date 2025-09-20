@echo off
REM Firefox Setup for Instagram Reels Extractor - Windows Batch Script

echo 🎬 Firefox Setup for Instagram Reels Extractor
echo ==============================================
echo This will create both bookmark files and a Firefox extension.
echo.

echo 📌 Creating Firefox bookmark files...
python create_firefox_bookmark.py
if %errorlevel% neq 0 (
    echo ❌ Error creating bookmark files
    pause
    exit /b 1
)

echo.
echo ========================================

echo 🔧 Creating Firefox extension...
python create_firefox_extension.py
if %errorlevel% neq 0 (
    echo ❌ Error creating extension
    pause
    exit /b 1
)

echo.
echo ==============================================
echo 📋 Setup Complete!
echo.
echo ✅ Bookmark files created in: firefox_bookmarks/
echo    - instagram_reels_bookmark.html (import this)
echo    - FIREFOX_BOOKMARK_INSTRUCTIONS.md (follow these)
echo.
echo ✅ Firefox extension created in: firefox_extension/
echo    - Load manifest.json in about:debugging
echo    - Or follow README.md for installation
echo.
echo 🎯 Choose your preferred method:
echo 1. 📌 Bookmark: Import the HTML file or follow manual instructions
echo 2. 🔧 Extension: Load the extension in Firefox for a toolbar button
echo.
echo 💡 Both methods will extract Reels URLs and copy them to clipboard!
echo.
pause
