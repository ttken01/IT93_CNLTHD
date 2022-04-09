import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './App.css';
import Home from './components/Home';
import Lesson from './components/Lesson';
import Header from './layout/Header';
import 'bootstrap/dist/css/bootstrap.min.css';
import Footer from './layout/Footer';

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/courses/:courseId/lessons" element={<Lesson />} />
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}

export default App;
