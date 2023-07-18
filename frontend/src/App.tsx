import React from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import { Sidebar } from "./components/sidebar";

import "./App.css";
import { Upload } from "./pages/Upload";
import { Selection } from "./pages/Selection";
import { Page404 } from "./pages/Page404";
import { AdditionalInfo } from "./pages/AdditionalInfo";
import { Training } from "./pages/Training";
import { Prediction } from "./pages/Prediction";

function App() {
  const base = process.env.REACT_APP_PREFIX;
  return (
    <Router basename={base}>
      <Sidebar />
      <main>
        <header>Predictive Process Monitoring - Next Event Prediction</header>
        <Routes>
          <Route path="/" element={<Upload />} />
          <Route path="/selection" element={<Selection />} />
          <Route path="/training" element={<Training />} />
          <Route path="/prediction" element={<Prediction />} />
          <Route path="/information" element={<AdditionalInfo />} />
          <Route path="*" element={<Page404 />} />
        </Routes>
      </main>
      <footer />
    </Router>
  );
}

export default App;
