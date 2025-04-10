import { useState } from "react";
import axios from "axios";
import { Upload } from "lucide-react";

export default function FileUploader({ setAnalysis }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a log file (.txt or .log) first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setAnalysis(response.data.analysis);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to process log file.");
    }
    setLoading(false);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "15px" }}>
      <input type="file" accept=".txt,.log" onChange={handleFileChange} style={{ border: "1px solid #d63384", padding: "10px", borderRadius: "5px", backgroundColor: "#fff0f5" }} />
      <button onClick={handleUpload} disabled={loading} style={{ padding: "10px 20px", backgroundColor: "#ff69b4", color: "white", borderRadius: "5px", border: "none", cursor: "pointer" }}>
        {loading ? "Uploading..." : <><Upload style={{ width: "16px", height: "16px", marginRight: "5px" }} /> Upload & Analyze</>}
      </button>
    </div>
  );
}
