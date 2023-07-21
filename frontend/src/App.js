import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from './components/NavBar';

import Classifier from './routes/Classifier'
import Recommender from './routes/Recommender'
import Axios from "axios";

Axios.defaults.baseURL = "http://127.0.0.1:8000/api/";

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route exact path="/" element={<Classifier />} />
        <Route exact path="/recommender" element={<Recommender />} />
      </Routes>
    </Router>
  )
}

export default App;