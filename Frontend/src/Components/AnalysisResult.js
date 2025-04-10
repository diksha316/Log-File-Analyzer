export default function AnalysisResult({ analysis }) {
    return (
      <div style={{ width: "100%", padding: "15px", marginTop: "15px", backgroundColor: "#ffc0cb", borderRadius: "5px" }}>
        <h3 style={{ fontSize: "18px", fontWeight: "bold", color: "#d63384" }}>Analysis Result:</h3>
        <pre style={{ fontSize: "14px", whiteSpace: "pre-wrap", color: "#800000" }}>{analysis}</pre>
      </div>
    );
  }
  