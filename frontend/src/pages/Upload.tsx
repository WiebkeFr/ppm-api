import React, { ChangeEvent, useState } from "react";
import axios from "axios";
import "bootstrap-icons/font/bootstrap-icons.css";
import { AdditionalInfoCsv } from "../types";

export const Upload = () => {
  const [file, setFile] = useState<File>();
  const [info, setInfo] = useState<AdditionalInfoCsv>({
    isWithHeader: false,
    delimiter: ",",
    caseIdColumn: 0,
    activityColumn: 1,
    timestampColumn: 2,
  });
  const [progress, setProgress] = useState(0);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (progress === -1) {
      setProgress(0);
    }
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleAddInfo = (e: ChangeEvent<HTMLInputElement>, id: string) => {
    setInfo((prevState) => ({
      ...prevState,
      [id]: e.target.checked,
    }));
  };

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("info", JSON.stringify(info));

    axios
      .post("/api/upload/event-logs", formData, {
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
      <p>Helptext</p>
      <h4>Upload</h4>
      <p>Helptext</p>

      <label htmlFor="fileUpload" className="form-label">
        Select XML-Testset (downloaded from CPEE.org)
      </label>
      <div className="d-flex mb-3">
        <input
          className="form-control file-upload-field"
          type="file"
          accept="text/xml/csv/xes"
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
      <div className="form-group row">
        <div className="col-sm-2">Checkbox</div>
        <div className="col-sm-10">
          <div className="form-check">
            <input
              className="form-check-input"
              type="checkbox"
              id="gridCheck1"
              onChange={(e) => handleAddInfo(e, "isWithHeader")}
            />
          </div>
        </div>
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
        <a href="/selection" style={{ display: "block" }}>
          <button className="border rounded my-5 p-2">
            Selection
            <i className="bi bi-arrow-right ps-2"></i>
          </button>
        </a>
      )}
    </div>
  );
};
