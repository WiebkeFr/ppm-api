import React from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import { Sidebar } from "./components/sidebar";

import "./App.css";
import { Upload } from "./pages/Upload";
import { Selection } from "./pages/Selection";
import { Page404 } from "./pages/Page404";
import { AdditionalInfo } from "./pages/AdditionalInfo";

function App() {
  return (
    <Router>
      <Sidebar />
      <main>
        <header>Predictive Process Monitoring - Next Event Prediction</header>
        <Routes>
          <Route path="/" element={<Upload />} />
          <Route path="/selection" element={<Selection />} />
          <Route path="/information" element={<AdditionalInfo />} />
          <Route path="*" element={<Page404 />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
