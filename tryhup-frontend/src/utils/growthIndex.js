// src/utils/growthIndex.js
// ================================
// Calcolo indice di crescita 🌰🌱🌿🌳
// ================================

export function growthIndex(ratingAvg, ratingCount) {
  if (ratingCount === 0) return "🌰"

  if (ratingAvg < 2.0) return "🌱"
  if (ratingAvg < 3.0) return "🌿"
  return "🌳"
}
