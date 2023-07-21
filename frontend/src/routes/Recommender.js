import React, { useState } from "react";
import axios from "axios";
import loadingIcon from "../image/Loading_icon.gif";

const Recommender = () => {
  const [formData, setFormData] = useState({
    description: "",
    top_k: 3,
  });
  const [isLoading, setIsLoading] = useState(false);

  const [recommendation, setRecommendation] = useState({});

  const handleChange = (e) => {
    setFormData((prevFormData) => {
      return { ...prevFormData, [e.target.name]: e.target.value };
    });
  };

  const { description, top_k } = formData;

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsLoading(true);
    axios
      .post("recommender/recommend/", {
        description,
        top_k,
      })
      .then((res) => {
        console.log("From Response");
        console.log(res.data);
        setRecommendation(res.data);
      })
      .catch((err) => {
        console.log("error occurred");
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const showRecommendation = () => {
    if (recommendation && recommendation.length > 0) {
      return recommendation.map((rec, index) => (
        <div className="card mb-3" key={index}>
          <div className="card-body">
            <h5 className="card-title">{rec.title}</h5>
            <h6 className="card-subtitle mb-2 text-muted">
              Authors: {rec.authors}
            </h6>
            <p className="card-text">{rec.abstract}</p>
            <p className="card-text">Categories: {rec.categories}</p>
            <p className="card-text">Comments: {rec.comments}</p>
            <p className="card-text">Date: {rec.date}</p>
            <p className="card-text">
              DOI: <a href={rec.doi}>{rec.doi}</a>
            </p>
            <p className="card-text">ID: {rec.id}</p>
            <p className="card-text">Submitter: {rec.submitter}</p>
          </div>
        </div>
      ));
    }
  };

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-md-12">
          <h2>Recommendation System</h2>
          <form onSubmit={(e) => handleSubmit(e)}>
            <div class="mb-3">
              <textarea
                type="text"
                className="form-control"
                id="description"
                name="description"
                placeholder="Write your description here..."
                rows="10"
                value={description}
                onChange={(e) => handleChange(e)}
              ></textarea>
            </div>
            <label for="tag_no" class="form-label">
              No. of Paper Recommendation
            </label>
            <input
              type="number"
              className="form-control mb-4"
              id="top_k"
              name="top_k"
              placeholder="Enter a number"
              value={top_k}
              onChange={(e) => handleChange(e)}
            />

            <button
              type="submit"
              className="form-control btn btn-success"
              disabled={isLoading}
            >
              {isLoading ? "Loading..." : "Recommend"}
            </button>
          </form>
        </div>
        {/* Recommended Paper Section */}

        {isLoading ? (
          <div className="col-md-12 text-center">
            <img src={loadingIcon} alt="Loading..." />
          </div>
        ) : (
          <div className="col-md-12 mt-2">{showRecommendation()}</div>
        )}
      </div>
    </div>
  );
};

export default Recommender;
