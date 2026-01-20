// 📚 Feed pubblico TryHup
// Mostra contenuti (video + immagini) approvati
// Layout verticale stile social editoriale

import React, { useEffect, useState } from "react";
import ContentCard from "../components/ContentCard";

export default function Feed() {
  // Stato contenuti
  const [contents, setContents] = useState([]);

  // Stato errore
  const [error, setError] = useState(null);

  // Caricamento feed
  useEffect(() => {
    fetch("http://127.0.0.1:8000/contents/feed")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Errore nel caricamento del feed");
        }
        return res.json();
      })
      .then((data) => {
        setContents(data);
      })
      .catch((err) => {
        setError(err.message);
      });
  }, []);

  return (
    <div
      style={{
        maxWidth: "480px",
        margin: "0 auto",
        padding: "16px",
      }}
    >
      {/* Titolo */}
      <h1 style={{ marginBottom: "24px", textAlign: "center" }}>
        🌳 Feed TryHup
      </h1>

      {/* Errore */}
      {error && (
        <p style={{ color: "red", textAlign: "center" }}>
          ❌ {error}
        </p>
      )}

      {/* Nessun contenuto */}
      {contents.length === 0 && !error && (
        <p style={{ textAlign: "center" }}>
          Nessun contenuto approvato disponibile.
        </p>
      )}

      {/* Feed verticale */}
      <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
        {contents.map((content) => (
          <ContentCard key={content.id} content={content} />
        ))}
      </div>
    </div>
  );
}
