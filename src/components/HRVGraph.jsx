import React, { useState } from "react";
import axios from "axios";

const HRVGraph = () => {
  const [graphUrl, setGraphUrl] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchGraph = async () => {
    try {
      setLoading(true); // Set loading state
      setError(null); // Clear previous errors
      const response = await axios.get("http://127.0.0.1:8001/generate_hrv_report/", {
        responseType: "blob", // Fetch as a file
      });

      // Convert blob to an object URL
      const url = window.URL.createObjectURL(response.data);
      setGraphUrl(url);
    } catch (err) {
      setError("Failed to fetch the graph. Please try again.");
    } finally {
      setLoading(false); // Reset loading state
    }
  };

  return (
    <div className="flex flex-col items-center mt-12">
      <h1 className="text-2xl font-bold mb-6">HRV Report</h1>
      <button
        onClick={fetchGraph}
        className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-all"
        disabled={loading} // Disable button while loading
      >
        {loading ? "Generating..." : "Generate HRV Graph"}
      </button>

      {error && <p className="text-red-500 mt-4">{error}</p>}

      {graphUrl && (
        <div className="mt-6 text-center">
          <h3 className="text-lg font-semibold mb-4">Your HRV Graph:</h3>
          <img
            src={graphUrl}
            alt="HRV Report Graph"
            className="w-full max-w-lg border border-gray-300 rounded-lg shadow-lg"
            onLoad={() => console.log("Image loaded successfully")}
            onError={() => setError("Error loading image. Please try again.")}
          />
          <div className="mt-4">
            <a
              href={graphUrl}
              download="hrv_report.png"
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-all"
            >
              Download Graph
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default HRVGraph;
