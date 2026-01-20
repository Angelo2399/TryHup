// 🌱 Indice di Crescita TryHup
// Usa 4 stadi naturali al posto di like o stelline

import React from "react";

// Mappa indice → icona + significato
function getGrowthData(value) {
  if (value <= 1) {
    return { emoji: "🌰", label: "Idea embrionale" };
  }
  if (value === 2) {
    return { emoji: "🌱", label: "Inizio crescita" };
  }
  if (value === 3) {
    return { emoji: "🌿", label: "Sviluppo" };
  }
  return { emoji: "🌳", label: "Maturità" };
}

// Componente principale
export default function GrowthIndex({ value }) {
  const { emoji, label } = getGrowthData(value);

  return (
    <div style={{ marginTop: "8px", display: "flex", alignItems: "center" }}>
      {/* Icona */}
      <span style={{ fontSize: "1.6rem", marginRight: "8px" }}>
        {emoji}
      </span>

      {/* Testo */}
      <div>
        <strong>{label}</strong>
        <div style={{ fontSize: "0.85rem", opacity: 0.7 }}>
          Indice di crescita: {value} / 4
        </div>
      </div>
    </div>
  );
}
