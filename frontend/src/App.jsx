import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Room from "./pages/Room";
import "./App.css";
function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/room/:roomCode" element={<Room />} />
    </Routes>
  );
}

export default App;