import { useEffect, useState } from "react"

export default function Rating({ videoId, onRated }) {
  const storageKey = `tryhup_rated_${videoId}`

  const [loading, setLoading] = useState(false)
  const [hasVoted, setHasVoted] = useState(false)
  const [hover, setHover] = useState(0)

  // ===============================
  // Controllo voto già effettuato
  // ===============================
  useEffect(() => {
    if (localStorage.getItem(storageKey)) {
      setHasVoted(true)
    }
  }, [storageKey])

  // ===============================
  // Invio voto (1–5)
  // ===============================
  const rate = async (value) => {
    if (loading || hasVoted) return

    setLoading(true)

    await fetch(`http://127.0.0.1:8000/videos/${videoId}/rate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ rating: value }),
    })

    localStorage.setItem(storageKey, "true")
    setHasVoted(true)
    setLoading(false)

    onRated()
  }

  // 🌰🌱🌿🌳 (valori visivi)
  const icons = ["🌰", "🌱", "🌿", "🌳"]

  // Mappatura UI → valore reale (1–5)
  const valueMap = {
    1: 1,
    2: 2,
    3: 3,
    4: 5, // 🌳 rappresenta il massimo
  }

  return (
    <div style={{ marginTop: "8px" }}>
      {hasVoted ? (
        <p style={{ fontStyle: "italic", opacity: 0.7 }}>
          ✅ Hai già votato
        </p>
      ) : (
        <div>
          {[1, 2, 3, 4].map((uiValue) => (
            <span
              key={uiValue}
              onMouseEnter={() => setHover(uiValue)}
              onMouseLeave={() => setHover(0)}
              onClick={() => rate(valueMap[uiValue])}
              style={{
                cursor: loading ? "not-allowed" : "pointer",
                fontSize: "22px",
                marginRight: "8px",
                opacity: hover >= uiValue ? 1 : 0.4,
                userSelect: "none",
              }}
            >
              {icons[uiValue - 1]}
            </span>
          ))}
        </div>
      )}
    </div>
  )
}
