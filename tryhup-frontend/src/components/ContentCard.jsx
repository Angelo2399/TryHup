import GrowthIndex from "./GrowthIndex";

export default function ContentCard({ content }) {
  return (
    <div
      style={{
        width: "100%",
        maxWidth: "420px",
        margin: "0 auto 24px",
        borderRadius: "12px",
        overflow: "hidden",
        background: "#111",
        color: "#fff",
      }}
    >
      {/* Media */}
      {content.media_type === "video" ? (
        <video
          src={content.media_url}
          controls
          style={{ width: "100%", display: "block" }}
        />
      ) : (
        <img
          src={content.media_url}
          alt=""
          style={{ width: "100%", display: "block" }}
        />
      )}

      {/* Testi */}
      <div style={{ padding: "12px" }}>
        <p style={{ marginBottom: "8px" }}>
          {content.creator_description}
        </p>

        {content.category && (
          <p style={{ opacity: 0.7, fontSize: "0.85rem" }}>
            #{content.category}
          </p>
        )}

        <GrowthIndex value={content.growth_index} />
      </div>
    </div>
  );
}
