const API_URL = "http://127.0.0.1:8000";

export async function fetchContentsFeed() {
  const res = await fetch(`${API_URL}/contents/feed`);
  if (!res.ok) {
    throw new Error("Errore nel caricamento del feed");
  }
  return res.json();
}
