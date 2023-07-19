import axios from "axios";
import React, { useState } from "react";

const Classifier = () => {
  const [formData, setFormData] = useState({
    abstract: "",
    tag_no: "",
  });

  const [predictionData, setPredictionData] = useState({});

  const handleChange = (e) => {
    setFormData((prevFormData) => {
      return { ...prevFormData, [e.target.name]: e.target.value };
    });
  };

  const { abstract, tag_no } = formData;

  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post("classfier/predict/", {
        abstract,
        tag_no,
      })
      .then((res) => {
        console.log("From Response");
        console.log(res.data);
        setPredictionData(res.data);
      })
      .catch((err) => {
        console.log("error occured");
      });
  };

  const showProgressBar = (value) => {
    value = value * 100;
    if (isNaN(value)) {
      value = 0;
    }
    let widthValue = value.toString() + "%";

    const widthStyle = { width: widthValue };

    return (
      <div className="progress mt-2" style={{ height: "3px" }}>
        <div
          className="progress-bar bg-info"
          role="progressbar"
          style={widthStyle}
          aria-valuenow="25"
          aria-valuemin="0"
          aria-valuemax="100"
        ></div>
      </div>
    );
  };

  const showPrediction = (data) => {
    console.log("From prediction: ", data);

    // Sort the data based on the value in descending order
    const sortedData = Object.entries(data).sort((a, b) => b[1] - a[1]);

    return (
      <div>
        {sortedData.map(([topic, value]) => (
          <div className="row mt-2" key={topic}>
            <div className="col-md-2">{topic}</div>
            <div className="col-md-8">{showProgressBar(value)}</div>
            <div className="col-md-2">{value.toFixed(2)}</div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <section>
      <div className="container mt-4">
        <div className="row">
          <div className="col-md-12">
            <h2>Topic Classifier</h2>
            <form onSubmit={(e) => handleSubmit(e)}>
              <div class="mb-3">
                <textarea
                  type="text"
                  class="form-control"
                  id="abstract"
                  name="abstract"
                  placeholder="Write your abstract here..."
                  rows="10"
                  value={abstract}
                  onChange={(e) => handleChange(e)}
                ></textarea>
              </div>
              <label for="tag_no" class="form-label">
                No. of Tags
              </label>
              <input
                type="number"
                class="form-control"
                id="tag_no"
                name="tag_no"
                placeholder="Enter a number"
                value={tag_no}
                onChange={(e) => handleChange(e)}
              />

              <button type="submit" className="form-control btn btn-success">
                Predict
              </button>
            </form>
          </div>
        </div>
        {/* end of first row  */}
        <div className="row">
          <div className="col-md-12">
            <div className="mt-4">
              <h3>Predictions</h3>
              {showPrediction(predictionData)}
            </div>
          </div>
        </div>
        {/* end of second row */}
      </div>
    </section>
  );
};

export default Classifier;
