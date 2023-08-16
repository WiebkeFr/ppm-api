import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Measurement,
  Measurement_Names,
  TrainingInfoOptions,
  TrainingInfoSelection,
} from "../types";
import { useNavigate } from "react-router-dom";

const initialTrainingOptions = TrainingInfoOptions.reduce(
  (obj, { key, options }) => {
    return {
      ...obj,
      [key]: options[0].key,
    };
  },
  {}
) as TrainingInfoSelection;

export const Selection = () => {
  const prefix = process.env.REACT_APP_PREFIX;
  const [measures, setMeasures] = useState<Measurement | {}>({});
  const [suggestion, setSuggestion] = useState("")
  const [error, setError] = useState<string>("");
  const [trainingInfo, setTrainingInfo] = useState<TrainingInfoSelection>(
    initialTrainingOptions
  );
  const [showModal, setShowModal] = useState(false);
  const navigate = useNavigate();

  const handleChange = (key: string, option: string) => {
    setTrainingInfo((prevState) => ({
      ...prevState,
      [key]: option,
    }));
  };

  useEffect(() => {
    if (Object.keys(measures).length === 0) {
      axios
        .get(prefix + "/api/evaluate/log")
        .then((res) => {
          console.log(res.data);
          setMeasures(res.data);
          getSuggestion()
        })
        .catch((error) => {
          console.log(error);
          setError(error.response.data.detail || error.message);
        });
    }
  });

  const getSuggestion = () => {
    axios
        .get(prefix + "/api/evaluate/selection")
        .then((res) => {
          console.log(res.data)
          setSuggestion(res.data.type);
        })
        .catch((error) => {
          console.log(error);
          setError(error.response.data.detail || error.message);
        });
  }

  const startTraining = () => {
    axios.post(prefix + "/api/train", trainingInfo).then((res) => {
      if (res.data.state === "warning-duplicate") {
        setShowModal(true);
      }
      if (res.data.state === "success") {
        navigate("/training");
      }
    });
  };

  const restartTraining = () => {
    axios.post(prefix + "/api/train?overwrite=true", trainingInfo);
    navigate(prefix + "/training");
  };

  return (
    <div>
      <h4 className="mt-4">Selection</h4>

      {error !== "" && (
        <div className="alert alert-danger d-inline-block mt-3" role="alert">
          {error}
        </div>
      )}

      {TrainingInfoOptions.map(({ label, key, options }) => (
        <div key={key}>
          <div className="fw-bolder mt-3">{label}:</div>
          {options.map((option) => (
            <div className="form-check">
              <input
                className="form-check-input"
                type="radio"
                name={option.key}
                id={option.key}
                onChange={(e) => handleChange(key, option.key)}
                checked={
                  trainingInfo[key as keyof TrainingInfoSelection] ===
                  option.key
                }
              />
              <label className="form-check-label" htmlFor={option.key}>
                {option.label}
              </label>
            </div>
          ))}
        </div>
      ))}

        {
            suggestion !== "" &&
            <div className="alert alert-info d-inline-block mt-4" role="alert"
                style={{ width: "70%" }}>
              Recommended Model Type: <b>{suggestion}</b><br/>
                If the process requires long-term dependencies <b>Prefix-Padded</b> Encoding is favorable.
                However, the training time of the <b>continous</b> encoded models are lower on average.
            </div>
        }
      <h4 className="mt-4">Characteristic of Event Log</h4>

      <table
        className="table table-striped"
        style={{ width: "70%", marginTop: "16px" }}
      >
        <tbody>
          {Object.entries(measures).map(([key, value]) => (
            <tr>
              <td>{Measurement_Names[key]}</td>
              <td>
                {value % 1 ? value.toFixed(3) : value}
                {key === "time" && " s"}
                {key === "unique_t" && "%"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {error === "" && Object.entries(measures).length === 0 && (
        <div className="d-flex justify-content-center">
          <div className="spinner-border" role="status"></div>
        </div>
      )}

      {error === "" && (
        <button className="border rounded my-5 p-2" onClick={startTraining}>
          Training
          <i className="bi bi-arrow-right ps-2"></i>
        </button>
      )}

      {showModal && (
        <div
          className="modal fade show d-block"
          id="exampleModal"
          tabIndex={-1}
          role="dialog"
          aria-labelledby="warning-overwrite-training"
          aria-hidden="true"
        >
          <div className="modal-dialog" role="document">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="warning-overwrite-training">
                  Warning
                </h5>
                <button
                  type="button"
                  className="close"
                  data-dismiss="modal"
                  aria-label="Close"
                  onClick={() => setShowModal(false)}
                >
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div className="modal-body">
                A trained model and results for your dataset already exist. Are
                you sure you want to repeat the training?
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowModal(false)}
                >
                  Close
                </button>
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={() => restartTraining()}
                >
                  Train again
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
