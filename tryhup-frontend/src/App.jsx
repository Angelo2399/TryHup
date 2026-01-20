// 🌳 App principale TryHup
// Orchestratore dell'applicazione
// La logica vive nei componenti/pagine

import Feed from "./pages/Feed";
import "./App.css";

function App() {
  return (
    <div
      style={{
        backgroundColor: "#000",
        minHeight: "100vh",
        color: "#fff",
      }}
    >
      {/* Header */}
      <header style={{ textAlign: "center", padding: "16px 0" }}>
        <h1>🌳 TryHup</h1>
        <p style={{ opacity: 0.7, fontSize: "0.9rem" }}>
          Social editoriale per scienza, tecnologia e società
        </p>
      </header>

      {/* Feed verticale */}
      <Feed />
    </div>
  );
}

export default App;
