import { useState } from "react";
import FileUploader from "../Components/FileUploader";
import AnalysisResult from "../Components/AnalysisResult";

export default function Home() {
  const [analysis, setAnalysis] = useState(null);

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "100vh", padding: "20px", backgroundColor: "#ffe4e1" }}>
      <div style={{ width: "100%", maxWidth: "500px", padding: "20px", boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)", borderRadius: "10px", backgroundColor: "#ffb6c1" }}>
        <h2 style={{ fontSize: "22px", fontWeight: "bold", color: "#d63384", textAlign: "center" }}>Log File Analyzer</h2>
        <FileUploader setAnalysis={setAnalysis} />
        {analysis && <AnalysisResult analysis={analysis} />}
      </div>
    </div>
  );
}
