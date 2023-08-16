import React, { ChangeEvent, useState } from "react";
import axios from "axios";
import "bootstrap-icons/font/bootstrap-icons.css";

export const Upload = () => {
  const prefix = process.env.REACT_APP_PREFIX;
  const [file, setFile] = useState<File>();
  const [progress, setProgress] = useState(0);

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
      .post(prefix + "/api/upload/event-logs", formData, {
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const progress = (progressEvent.loaded / progressEvent.total) * 100;
            setProgress(progress);
          }
        },
      })
      .then((res) => {
        console.log(res);
      })
      .catch((error) => {
        console.log(error.message);
        setProgress(-1);
      });
  };

  return (
    <div>
      <h4 className="mt-4">How to upload the event log?</h4>
        <br/>
      <p>
        Event log can be uploaded as a <b>XES</b> or <b>CSV</b> files.
        <br/>
        A CSV <b>needs</b> to contain the three columns in the right sequence:
      </p>
        <table className="table table-bordered w-75">
            <tr>
                <td className="text-center">Case ID</td>
                <td className="text-center">Event ID</td>
                <td className="text-center">Timestamp (optional)</td>
              </tr>
        </table>
        <p>The XES needs to be structured according to the <a href="http://www.xes-standard.org/">XES-Standard</a>.</p>
        <br/>
        <p>
        Alternatively, a <b>XML</b> file of process can be uploaded.<br/>
        The file is a downloaded testset from <a href="https://cpee.org/">Cloud Process Execution Engine (CPEE)</a>. <br/>
        The Engine is then used to create traces. (Depending on the testset this can take some time.)
      </p>
        <br/>
      <label htmlFor="fileUpload" className="form-label">
          <b>Select CSV/XES or XML file:</b>
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
          Upload
          <i className="bi bi-upload ps-2"></i>
        </button>
      </div>
      {progress === 100 && (
        <div className="alert alert-success d-inline-block mt-3" role="alert">
          Successfully uploaded!
        </div>
      )}
      {progress === -1 && (
        <div className="alert alert-danger d-inline-block  mt-3" role="alert">
          Something went wrong, please try again!
        </div>
      )}
      {progress > 0 && progress < 100 && (
        <div className="progress w-50 mt-2">
          <div
            className="progress-bar progress-bar-striped progress-bar-animated"
            role="progressbar"
            style={{ width: progress + "%" }}
            aria-valuenow={progress}
            aria-valuemin={0}
            aria-valuemax={100}
          >
            {Math.round(progress)}%
          </div>
        </div>
      )}
      {progress === 100 && (
        <a href={prefix + "/selection"} style={{ display: "block" }}>
          <button className="border rounded my-5 p-2">
            Selection
            <i className="bi bi-arrow-right ps-2"></i>
          </button>
        </a>
      )}
    </div>
  );
};
