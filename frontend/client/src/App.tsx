import { useState } from "react";

type Job = {
  job_id: string;
  title: string;
  company: string;
  location: string;
  apply_url: string;
  poe: number;
};

function App() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedJobs, setSelectedJobs] = useState<Set<string>>(new Set());
  const [resumeFile, setResumeFile] = useState<File | null>(null);

  // -------------------------
  // Discover jobs
  // -------------------------
  const discoverJobs = async () => {
    setLoading(true);

    const res = await fetch("http://127.0.0.1:8000/jobs/discover", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        target_roles: ["ml engineer", "data scientist"],
        core_skills: ["machine learning", "deep learning", "pytorch"],
        location: ["US"],
      }),
    });

    const data = await res.json();
    setJobs(data);
    setLoading(false);
  };

  // -------------------------
  // Generate cover letters
  // -------------------------
  const generateCoverLetters = async () => {


    console.log("CLICKED generateCoverLetters");
    console.log("resumeFile =", resumeFile);

    if (!resumeFile) {
      alert("Upload your resume PDF first");
      return;
    }

    if (selectedJobs.size === 0) {
      alert("Select at least one job");
      return;
    }

    const form = new FormData();
    form.append("resume", resumeFile);

    selectedJobs.forEach((id) => {
      form.append("job_ids", id);
    });

    const res = await fetch("http://127.0.0.1:8000/jobs/cover-letter", {
      method: "POST",
      body: form, // ❗ no headers
    });

    if (!res.ok) {
      alert("Failed to generate cover letters");
      return;
    }

    const files: { filename: string }[] = await res.json();

    files.forEach((f) => {
      window.open(`http://127.0.0.1:8000/files/${f.filename}`, "_blank");
    });
  };

  // -------------------------
  // UI
  // -------------------------
  return (
    <div style={{ padding: "2rem", color: "white" }}>
      <h1>Job Agent</h1>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => {
          const file = e.target.files?.[0] || null;
          setResumeFile(file);
        }}
      />

      <button onClick={discoverJobs}>
        {loading ? "Loading..." : "Discover Jobs"}
      </button>

      <hr />

      {jobs.map((job) => (
        <div key={job.job_id} style={{ marginBottom: "1rem" }}>
          <input
            type="checkbox"
            checked={selectedJobs.has(job.job_id)}
            onChange={() => {
              const next = new Set(selectedJobs);
              next.has(job.job_id)
                ? next.delete(job.job_id)
                : next.add(job.job_id);
              setSelectedJobs(next);
            }}
          />

          <h3>{job.title}</h3>
          <p>
            {job.company} · {job.location}
          </p>
          <p>PoE score: {job.poe.toFixed(3)}</p>
          <a href={job.apply_url} target="_blank" rel="noreferrer">
            Apply
          </a>
        </div>
      ))}

      {jobs.length > 0 && (
        <>
          <hr />
          <button onClick={generateCoverLetters}>
            Generate Cover Letters
          </button>
        </>
      )}
    </div>
  );
}

export default App;
