import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

function App() {
  const [sessions, setSessions] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const threadEndRef = useRef(null);

  const activeSession = sessions.find((s) => s.id === activeId) || null;


  useEffect(() => {
    fetch("http://127.0.0.1:8000/sessions")
      .then((r) => r.json())
      .then((data) =>
        setSessions(
          data.map((s) => ({
            id: s.id,
            image: s.image,
            messages: s.messages,
            createdAt: new Date(s.created_at),
          }))
        )
      )
      .catch((err) => console.error("Failed to load sessions", err));
  }, []);

  useEffect(() => {
  const interval = setInterval(() => {
    fetch("http://127.0.0.1:8000/sessions")
      .then((r) => r.json())
      .then((data) => {
        setSessions((prev) => {
          // only update if the session count actually changed, avoid flicker
          if (data.length !== prev.length) {
            return data.map((s) => ({
              id: s.id,
              image: s.image,
              messages: s.messages,
              createdAt: new Date(s.created_at),
            }));
          }
          return prev;
        });
      })
      .catch(() => {});
  }, 3000); // check every 3 seconds

  return () => clearInterval(interval);
}, []);

  useEffect(() => {
    threadEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeSession?.messages, loading]);

  const captureScreen = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/capture", { method: "POST" });
      const data = await response.json();
      const newSession = { id: data.session_id, image: data.image, messages: [], createdAt: new Date() };
      setSessions((prev) => [newSession, ...prev]);
      setActiveId(newSession.id);
      setQuestion("");
    } catch (error) {
      console.error("Capture failed", error);
    }
  };

  const selectArea = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/select-area", { method: "POST" });
      const data = await response.json();
      if (data.session_id) {
        const newSession = { id: data.session_id, image: data.image, messages: [], createdAt: new Date() };
        setSessions((prev) => [newSession, ...prev]);
        setActiveId(newSession.id);
        setQuestion("");
      }
    } catch (error) {
      console.error("Select area failed", error);
    }
  };

  const resetScreenSense = () => {
    setActiveId(null);
    setQuestion("");
  };

  const deleteHistory = async () => {
  if (!window.confirm("Delete all history?")) return;

  try {
    await fetch("http://127.0.0.1:8000/sessions", {
      method: "DELETE",
    });

    setSessions([]);
    setActiveId(null);
    setQuestion("");
  } catch (error) {
    console.error("Failed to delete history", error);
  }
};


  const openSession = (id) => {
    setActiveId(id);
    setQuestion("");
  };

  const askScreenSense = async () => {
    if (!question.trim() || !activeSession) return;

    const userMessage = { role: "user", text: question };
    setSessions((prev) =>
      prev.map((s) => (s.id === activeSession.id ? { ...s, messages: [...s.messages, userMessage] } : s))
    );
    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMessage.text, session_id: activeSession.id }),
      });
      const data = await response.json();
      const modelMessage = { role: "model", text: data.answer };

      setSessions((prev) =>
        prev.map((s) =>
          s.id === activeSession.id ? { ...s, messages: [...s.messages, modelMessage] } : s
        )
      );
    } catch (error) {
      const errMessage = { role: "model", text: "❌ Could not connect to ScreenSense backend." };
      setSessions((prev) =>
        prev.map((s) =>
          s.id === activeSession.id ? { ...s, messages: [...s.messages, errMessage] } : s
        )
      );
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <div className="header">
        <h1>👁️ ScreenSense</h1>
        <p>Your AI that understands your screen.</p>
      </div>

      <div className="layout">
        <aside className="sidebar">
          <h4>History</h4>
          <button className="delete-history" onClick={deleteHistory}>
            🗑️ Delete History
          </button>
          {sessions.length === 0 ? (
            <p className="sidebar-empty">Captures you take will show up here.</p>
          ) : (
            <ul className="session-list">
              {sessions.map((s) => (
                <li
                  key={s.id}
                  className={s.id === activeId ? "session-item active" : "session-item"}
                  onClick={() => openSession(s.id)}
                >
                  <img src={s.image} alt="" />
                  <div className="session-meta">
                    <span className="session-title">
                      {s.messages[0]?.text || "New capture"}
                    </span>
                    <span className="session-time">
                      {s.createdAt.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </aside>

        <div className="card">
          <div className="toolbar">
            <button className="capture" onClick={captureScreen}>
              📸 Capture Screen
            </button>
            <button className="select-area" onClick={selectArea}>
              🎯 Select Area
            </button>
            <button className="reset" onClick={resetScreenSense} title="Reset">
              🔄
            </button>
          </div>

          {activeSession ? (
            <>
              <div className="preview">
                <img src={activeSession.image} alt="Captured screen" />
              </div>

              <div className="thread">
                {activeSession.messages.length === 0 && !loading && (
                  <p className="placeholder">Ask something about this capture to get started.</p>
                )}

                {activeSession.messages.map((m, i) => (
                  <div key={i} className={`bubble ${m.role}`}>
                    {m.role === "model" ? (
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.text}</ReactMarkdown>
                    ) : (
                      <p>{m.text}</p>
                    )}
                  </div>
                ))}

                {loading && (
                  <div className="bubble model loading-bubble">
                    <div className="loading-pulse" aria-label="Analyzing your screen">
                      <span />
                      <span />
                      <span />
                    </div>
                  </div>
                )}
                <div ref={threadEndRef} />
              </div>

              <div className="question-box">
                <input
                  type="text"
                  placeholder="Ask a follow-up..."
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && askScreenSense()}
                />
                <button className="ask" onClick={askScreenSense} title="Ask">
                  ➤
                </button>
              </div>
            </>
          ) : (
            <div className="empty-state">
              <p>Capture your screen to start a conversation.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;