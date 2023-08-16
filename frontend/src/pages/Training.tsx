import React, { useEffect, useState } from "react";
import axios from "axios";

const TRAINING_ERROR =
  "An error occurred while training!\nPlease make sure you uploaded a correct dataset and chose a valid selection of model-type and encodings.";
const EVALUATION_ERROR =
  '<div class="alert alert-danger d-inline-block mt-3" role="alert">error occurred while training</div>';

export const Training = () => {
  const prefix = process.env.REACT_APP_PREFIX;
  const [confusionMatrix, setConfusionMatrix] = useState("");
  const [trainingHistory, setTrainingHistory] = useState("");
  const [report, setReport] = useState({});

  const [state, setState] = useState<
    "training" | "evaluate" | "success" | "error"
  >("training");
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      axios
        .get(prefix + "/api/train/training-progress")
        .then((res) => {
          console.log(res.data);
          if (
            res.data?.state === "training" ||
            res.data?.state === "evaluate"
          ) {
            setState(res.data?.state);
            setProgress(parseFloat(res.data.progress) * 100);
          } else if (res.data?.state === "error") {
            setState("error");
            setProgress(-1);
            clearInterval(interval);
          } else if (res.data?.state === "success") {
            setState("success");
            setProgress(100);
            getTrainingData();
            clearInterval(interval);
          } else {
            console.log(res.data);
            setProgress(100);
            clearInterval(interval);
          }
        })
        .catch((error) => {
          setState("error");
          setProgress(-1);
          console.log(error);
          clearInterval(interval);
        });
    }, 10000);
  });

  const getTrainingData = () => {
    if(confusionMatrix === ""){
      axios
      .get(prefix + "/api/evaluate/confusion-matrix")
      .then((res) => {
        setConfusionMatrix(res.data);
      })
      .catch(() => {
        setConfusionMatrix(EVALUATION_ERROR);
      });
    }

    if(trainingHistory === ""){
      axios
      .get(prefix + "/api/evaluate/training-history")
      .then((res) => {
        setTrainingHistory(res.data);
      })
      .catch(() => {
        setTrainingHistory(EVALUATION_ERROR);
      });
    }

    if(JSON.stringify(report) === "{}"){
      axios
      .get(prefix + "/api/evaluate/classification-report")
      .then((res) => {
        setReport(res.data);
      })
      .catch(() => {
        setReport(EVALUATION_ERROR);
      });
    }
  };

  const getTableRow = (key: string, values: Object | number) => {
    return (
      <tr>
        <th>{key}</th>
        {typeof values === "number" ? (
          <td colSpan={4}>{Math.round((values as number) * 100) / 100}</td>
        ) : (
          Object.values(values).map((v) => (
            <td>{Math.round((v as number) * 100) / 100}</td>
          ))
        )}
      </tr>
    );
  };

  return (
    <div>
      {state === "error" && progress === -1 && (
        <div className="alert alert-danger d-inline-block mt-3" role="alert">
          {TRAINING_ERROR}
        </div>
      )}
      {progress >= 0 && (
        <div className="d-flex my-3 align-items-center">
          <h4 className="my-2">Training Progress:</h4>
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

      {progress === 100 && (
        <>
          <h4 className="my-2">Training Results: </h4>
          {state === "evaluate" && (
            <div className="d-flex flex-column justify-content-center align-items-center">
              <div className="spinner-border" role="status" />
              <div>Evaluating model...</div>
            </div>
          )}
          {state === "error" && (
            <div
              className="alert alert-danger d-inline-block mt-3"
              role="alert"
            >
              {EVALUATION_ERROR}
            </div>
          )}
          <div className="container">
            <div className="row">
              <div className="col m-auto">
                <div
                  className="svg-container"
                  dangerouslySetInnerHTML={{ __html: trainingHistory }}
                />
              </div>
              <div className="col m-auto">
                <table className="table table-bordered w-100">
                  <tbody>
                    {Object.entries(report).map(([key, value], index) => {
                      if (index === 0) {
                        return (
                          <>
                            <tr>
                              <th />
                              {Object.keys(value as Object).map((k) => (
                                <th>{k}</th>
                              ))}
                            </tr>
                            {getTableRow(key, value as Object)}
                          </>
                        );
                      }
                      return getTableRow(key, value as Object);
                    })}
                  </tbody>
                </table>
              </div>
            </div>
            <div className="row mt-5">
              <div className="col m-auto">
                <div
                  className="svg-container"
                  dangerouslySetInnerHTML={{ __html: confusionMatrix }}
                />
              </div>
              <div className="col m-auto w-50 text-wrap">
                Further explanation on the metrics can be found under the following links: <br/>
                <a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html">
                  Scikit-Learn: Confusion Matrix
                </a>
                <br/>
                <a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html">
                  Classification Report
                </a>
                <br/>
                <a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html">Accuracy</a>
                <br/>
                <a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html">Precision</a>
                <br/>
                <a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html">Recall</a>
                <br/>
                <a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html">F1-Score</a>
              </div>
            </div>
          </div>
        </>
      )}

      {"success" === state && (
        <a href={prefix + "/prediction"} style={{ display: "block" }}>
          <button className="border rounded my-5 p-2">
            Prediction
            <i className="bi bi-arrow-right ps-2"></i>
          </button>
        </a>
      )}

    </div>
  );
};
