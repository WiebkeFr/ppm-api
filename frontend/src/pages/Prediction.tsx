import React, { ChangeEvent, useState } from "react";
import axios from "axios";

export const Prediction = () => {
  const prefix = process.env.REACT_APP_PREFIX;
  const [file, setFile] = useState<File>();
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string>("");
  const [result, setResult] = useState({"next_event": "", process: []})

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (progress === -1) {
      setProgress(0);
    }
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    axios
      .post(prefix + "/api/predict", formData, {
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const progress = (progressEvent.loaded / progressEvent.total) * 100;
            setProgress(progress);
          }
        },
      })
      .then((res) => {
        console.log(res.data);
        setResult(res.data)
      })
      .catch((error) => {
        console.log(error);
        setProgress(-1);
        setError(error.response.data.detail || error.message);
      });
  };

  return (
    <div>
      <h4 className="mt-4">Execution of Prediction</h4>
      <label htmlFor="fileUpload" className="form-label">
        Upload the unfinished process as a XES/CSV file (same format as the event log)
      </label>
      <div className="d-flex mb-3">
        <input
          className="form-control file-upload-field"
          type="file"
          accept="xml/csv/xes"
          id="fileUpload"
          onChange={handleFileChange}
        />
        <button
          className="border rounded ms-3"
          type="submit"
          onClick={uploadFile}
        >
          Predict
          <i className="bi bi-upload ps-2"></i>
        </button>
      </div>
      { progress > 0 && progress < 100 && (
        <div className="d-flex my-3 align-items-center">
        <h4 className="my-2">Upload Progress:</h4>
        <div className="progress w-50 ms-3">
          <div
            className={
              "progress-bar progress-bar-striped" +
              (progress === 100 ? "" : " progress-bar-animated")
            }
            role="progressbar"
            style={{ width: progress + "%" }}
            aria-valuenow={Math.round(progress)}
            aria-valuemin={0}
            aria-valuemax={100}
          >
            {Math.round(progress)}%
          </div>
        </div>
      </div>
      )}
      {error !== "" && (
        <div className="alert alert-danger d-inline-block mt-3" role="alert">
          {error}
        </div>
      )}
      {
        result.next_event != "" && result.process.length != 0 &&
          <div className="d-flex">
            <div className="me-4 mt-4">
              <h4>Ongoing Process</h4>
              <table>
                    {
                      result.process.map(event => <tr>{event}</tr>)
                    }
              </table>
            </div>
            <div className="vr"></div>
            <div className="mt-4">
              <h4>Next Event</h4>
                <table>
                    <tr>{result.next_event}</tr>
                </table>
            </div>
          </div>
      }

    </div>
  );
};
