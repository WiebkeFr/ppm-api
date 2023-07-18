import React, {ChangeEvent, useState} from "react";
import axios from "axios";

export const Prediction = () => {
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
      .post("/api/predict", formData, {
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
      <h4>Execution of Prediction</h4>
      <label htmlFor="fileUpload" className="form-label">
        Upload XES-File of unfinished proces
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
          Predict
          <i className="bi bi-upload ps-2"></i>
        </button>
      </div>
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
    </div>
  );
};
