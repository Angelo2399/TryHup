import GrowthIndex from "./GrowthIndex";
import "./ContentCard.css";

export default function ContentCard({ content }) {
  const isVideo = content?.media?.type === "video";
  return (
    <div className="content-card">
      <div className="content-media">
        {isVideo ? (
          <video src={content.media.url} controls />
        ) : (
          <img src={content.media.url} alt={content.title || ""} />
        )}
      </div>
      <div className="content-body">
        <h2 className="content-title">{content.title}</h2>
        <p className="content-description">{content.description}</p>
        <GrowthIndex value={content.growthIndex} />
      </div>
    </div>
  );
}
