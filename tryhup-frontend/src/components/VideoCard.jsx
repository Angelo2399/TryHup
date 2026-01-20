// # Card che rappresenta un singolo video nel feed pubblico
// # Mostra contenuto + Indice di Crescita (niente like / stelline)

import React from "react";
import GrowthIndex from "./GrowthIndex";

export default function VideoCard({ video }) {
  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: "12px",
        padding: "16px",
        marginBottom: "16px",
        backgroundColor: "#fff",
        boxShadow: "0 2px 6px rgba(0,0,0,0.05)"
      }}
    >
      {/* # Titolo del video */}
      <h3 style={{ marginBottom: "8px" }}>{video.title}</h3>

      {/* # Descrizione */}
      <p style={{ marginBottom: "12px", color: "#444" }}>
        {video.description}
      </p>

      {/* # Autore / creator */}
      <div style={{ fontSize: "0.85rem", color: "#666" }}>
        Creato da <strong>{video.creator_name}</strong>
      </div>

      {/* # Indice di crescita (valore pubblico) */}
      <GrowthIndex value={video.growth_index ?? 0} />
    </div>
  );
}
