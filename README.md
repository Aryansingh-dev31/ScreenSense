# ScreenSense 🖥️🤖

**An AI-powered screen assistant that helps you understand, analyze, and troubleshoot what's on your screen.**

ScreenSense combines screenshot capture with AI-powered visual question answering to help users understand screen content, investigate coding errors, and get contextual assistance.

## ✨ Features

- 📸 **Screenshot Capture:** Capture screen content for AI analysis.
- 🎯 **Region Selection:** Select a specific area of your screen for focused assistance.
- 🤖 **AI-Powered Q&A:** Ask questions about screenshots using Google's Gemini API.
- ⌨️ **Global Keyboard Shortcut:** Trigger screenshot capture with `Ctrl + Shift + X`.
- 🗂️ **Screenshot History:** Access captured screenshots associated with sessions.
- 💬 **Contextual Assistance:** Get explanations based on the content of your screen.
- 🔄 **Session Management:** Manage screenshot sessions and history.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite, JavaScript |
| Backend | Python, FastAPI |
| AI | Google Gemini API |
| Database | SQLite |
| Screenshot Capture | PyAutoGUI |
| Keyboard Listener | Python `keyboard` library |

## 📁 Project Structure

```text
ScreenSense/
├── backend/
│   ├── main.py
│   ├── screen_selector.py
│   └── requirement.txt
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
├── .gitignore
├── README.md
├── package.json
└── package-lock.json
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js and npm
- A Google Gemini API key

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ScreenSense
```

Replace the placeholder with your actual repository URL.

### 2. Set up the backend

From the project root, activate your Python virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r backend/requirement.txt
```

Create a `.env` file in the location expected by the backend and configure your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Never upload your real API key to GitHub.**

### 3. Run the backend

```powershell
cd backend
uvicorn main:app --reload
```

API documentation: http://127.0.0.1:8000/docs

### 4. Run the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, typically http://localhost:5173.

Keep both the frontend and backend running while using ScreenSense.

## ⌨️ Keyboard Shortcut

Press `Ctrl + Shift + X` to trigger screenshot capture while the backend's keyboard listener is running.

The shortcut currently captures the full screen. Region selection is available separately.

## 🔐 Security and Privacy

- Store API keys in environment variables.
- Keep `.env`, virtual environments, local databases, and private screenshots out of GitHub.
- Review screenshots before sharing them, as they may contain sensitive information.
- The current application is designed for local use; online deployment may require changes to desktop screenshot functionality.

## 🔮 Future Improvements

- Proactive assistance while working.
- Improved code-error detection and debugging.
- More robust session and screenshot management.
- Configurable capture and privacy controls.
- Secure remote deployment.

## 📄 License

A license has not yet been specified. Add a `LICENSE` file when you decide how others may use, modify, and distribute the project.

---

**ScreenSense — making screen-based problem-solving smarter.** 🚀