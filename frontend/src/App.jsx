import './App.css'
import {BrowserRouter, Route, Routes} from "react-router-dom"
import LandingPage from "./pages/landing-page.jsx"
import ChooseLevel from "./pages/choose-level.jsx";
import SolveQuestion from "./pages/solve-question.jsx";


function App() {
  return (
    <>
      <BrowserRouter>
          <Routes>
            <Route path="/" element={<LandingPage/>}/>
            <Route path="/choose-level" element={<ChooseLevel/>}/>
            <Route path="/solve-question" element={<SolveQuestion/>}/>
          </Routes>
        </BrowserRouter>
    </>
  )
}

export default App
