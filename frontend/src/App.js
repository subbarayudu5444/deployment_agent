import React, { useState } from "react";
import { API_URL } from "./config";

function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleDeploy = async () => {
    if (!repoUrl.startsWith("https://github.com/")) {
      setMessage("Invalid GitHub repository URL");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API_URL}/deploy`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ repo_url: repoUrl }),
      });

      const data = await response.json();
      setMessage(data.frontend_link ? `Deployment successful: ${data.frontend_link}` : data.error);
    } catch (error) {
      setMessage("Deployment failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Deployment Agent</h1>
      <input
        type="text"
        placeholder="Enter GitHub Repository URL"
        value={repoUrl}
        onChange={(e) => setRepoUrl(e.target.value)}
      />
      <button onClick={handleDeploy} disabled={loading}>
        {loading ? "Deploying..." : "Deploy"}
      </button>
      <p>{message}</p>
    </div>
  );
}

export default App;
