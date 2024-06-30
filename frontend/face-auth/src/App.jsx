import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AuthPage from './AuthPage';
import RegisterPage from './Register';
import Navigation from './Navigation';  

function App() {
  return (
    <Router>
      <div>
        <Navigation />  
        <Routes>
          <Route path="/auth" element={<AuthPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
