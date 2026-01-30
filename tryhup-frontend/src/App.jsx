import Feed from "./pages/Feed";
import "./App.css";

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">TryHup</h1>
        <p className="app-subtitle">Social editorial for science, technology and society</p>
      </header>
      <Feed />
    </div>
  );
}

export default App;
