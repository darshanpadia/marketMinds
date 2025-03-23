import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      {/* You can add more routes here later */}
    </Routes>
  );
}

export default App;
