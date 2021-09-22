import React, { useState } from "react";
// Import the main component
import { Viewer } from "@react-pdf-viewer/core"; // install this library
// Plugins
import { defaultLayoutPlugin } from "@react-pdf-viewer/default-layout"; // install this library
// Import the styles
import "@react-pdf-viewer/core/lib/styles/index.css";
import "@react-pdf-viewer/default-layout/lib/styles/index.css";
// Worker
import { Worker } from "@react-pdf-viewer/core"; // install this library
import axios from "axios";

export const App = () => {
  // Create new plugin instance
  const defaultLayoutPluginInstance = defaultLayoutPlugin();

  const [filePdf, setFilePdf] = useState(null);

  const [summary, setSummary] = useState("");

  // for onchange event
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfFileError, setPdfFileError] = useState("");

  // for submit event
  const [viewPdf, setViewPdf] = useState(null);

  // onchange event
  const fileType = ["application/pdf"];

  const handlePdfFileChange = (e) => {
    let selectedFile = e.target.files[0];
    setFilePdf(e.target.files[0]);
    if (selectedFile) {
      if (selectedFile && fileType.includes(selectedFile.type)) {
        let reader = new FileReader();
        reader.readAsDataURL(selectedFile);
        reader.onloadend = (e) => {
          setPdfFile(e.target.result);
          setPdfFileError("");
        };
      } else {
        setPdfFile(null);
        setPdfFileError("Please select valid pdf file");
      }
    } else {
      console.log("select your file");
    }
  };

  // form submit
  const handlePdfFileSubmit = (e) => {
    e.preventDefault();
    if (pdfFile !== null) {
      setViewPdf(pdfFile);
      let file = filePdf;
      const formData = new FormData();

      formData.append("file", file);

      console.log(file);

      axios
        .post("http://localhost:5000/summary", formData)
        .then((res) => {
          console.log(res.data.summary);
          setSummary(res.data.summary);
        })
        .catch((err) => console.warn(err));
    } else {
      setViewPdf(null);
    }
  };

  return (
    <div className="container">
      <br></br>

      <form className="form-group" onSubmit={handlePdfFileSubmit}>
        <input
          type="file"
          name="file"
          className="form-control"
          required
          onChange={handlePdfFileChange}
        />
        {pdfFileError && <div className="error-msg">{pdfFileError}</div>}
        <br></br>
        <button type="submit" className="btn btn-success btn-lg">
          UPLOAD
        </button>
      </form>
      <br></br>
      <h4>View PDF :</h4>
      <div className="pdf-container">
        {/* show pdf conditionally (if we have one)  */}
        {viewPdf && (
          <>
            <Worker workerUrl="https://unpkg.com/pdfjs-dist@2.6.347/build/pdf.worker.min.js">
              <Viewer
                fileUrl={viewPdf}
                plugins={[defaultLayoutPluginInstance]}
              />
            </Worker>
          </>
        )}

        {/* if we dont have pdf or viewPdf state is null */}
        {!viewPdf && <>No pdf file selected</>}
      </div>
      <br />
      <h4>Summary :</h4>
      <br />
      <div className="summaryContainer">
        <div className="summary">{summary}</div>
      </div>
    </div>
  );
};

export default App;
