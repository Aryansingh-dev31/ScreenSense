# ScreenSense 🖥️🤖

**An AI-powered screen assistant that helps you understand what's happening on your screen.**

ScreenSense lets you capture your screen, ask questions about what you're seeing, and receive AI-generated explanations and assistance. Whether you're debugging code, understanding an error, or exploring unfamiliar content, ScreenSense helps you make sense of your screen.

## ✨ Features

- **📸 Screenshot Capture** — Capture your screen and use it as context for your questions.
- **🎯 Area Selection** — Select a specific portion of your screen when you only need help with part of it.
- **🤖 AI-Powered Assistance** — Ask questions about screenshots and receive answers powered by Google's Gemini AI.
- **⌨️ Global Keyboard Shortcut** — Press `Ctrl + Shift + X` to trigger screenshot capture.
- **💬 Contextual Q&A** — Get explanations and assistance based on captured screen content.
- **🗂️ Screenshot History** — Access screenshots associated with your sessions.
- **🔄 Session Management** — Organize your interactions and manage screenshot history.
- **🌐 Web-Based Interface** — Interact with the assistant through a React frontend connected to a FastAPI backend.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite, JavaScript |
| Backend | Python, FastAPI |
| AI Model | Google Gemini API |
| Database | SQLite |
| Screenshot Capture | PyAutoGUI |
| Keyboard Shortcuts | Python `keyboard` library |
| API Communication | REST API |

## 📁 Project Structure

```text
ScreenSense/
├── backend/
│   ├── main.py
│   ├── screen_selector.py
│   ├── screenshots/
│   └── screensense.db
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── venv/
├── .gitignore
└── README.md
```

*The structure above is illustrative; your actual files may differ.*

## ⚙️ Prerequisites

Before running ScreenSense, make sure you have:

- Python 3.10 or later
- Node.js and npm
- A Google Gemini API key
- Git (optional, for cloning the repository)

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ScreenSense
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's actual URL.

### 2. Configure the backend

Open a terminal in the project root.

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```powershell
pip install fastapi "uvicorn[standard]" google-genai python-dotenv keyboard pyautogui pillow
```

If your project has a `requirements.txt`, you can install the pinned dependencies instead:

```powershell
pip install -r backend/requirements.txt
```

Create a `.env` file in the location from which your backend loads environment variables, and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the example value with your own API key. Never commit this file to GitHub.

### 3. Start the backend

Open a terminal in the backend directory:

```powershell
cd backend
uvicorn main:app --reload
```

The API should be available at:

`http://127.0.0.1:8000`

You can also explore the API documentation at:

`http://127.0.0.1:8000/docs`

### 4. Configure and start the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, usually:

`http://localhost:5173`

Keep both the backend and frontend running while using ScreenSense.

## ⌨️ Keyboard Shortcut

| Shortcut | Action |
|---|---|
| `Ctrl + Shift + X` | Trigger screenshot capture |

The global shortcut requires the backend process to be running. If it does not work, check whether the keyboard listener started successfully and whether Windows permissions or another application are interfering.

**Note:** The global shortcut currently captures the full screen. Use the area-selection functionality when you need to focus on a specific region.

## 🔐 Security and Privacy

- Keep your Gemini API key in an environment variable; never hardcode it in source code.
- Add `.env`, virtual environments, local databases, and generated screenshots to `.gitignore` where appropriate.
- Screenshots may contain sensitive information. Review them before sharing or uploading them.
- API keys and personal screen content should not be committed to a public repository.

## 🔮 Future Improvements

Potential improvements include:

- Proactive assistance while working.
- Better code-error detection and debugging workflows.
- More robust screenshot and session management.
- Improved privacy controls and configurable capture options.
- Secure deployment for remote access.

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome. Fork the repository, create a feature branch, and submit a pull request.

## 📄 License

Choose a license before distributing the project. For example, the MIT License allows broad reuse with attribution; add a `LICENSE` file if you choose it.

---

**Built to make screen-based problem-solving smarter, faster, and easier.** 🚀