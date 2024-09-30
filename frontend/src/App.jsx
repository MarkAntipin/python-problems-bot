import './App.css'
import {BrowserRouter, Route, Routes} from "react-router-dom"
import LandingPage from "./pages/landing-page.jsx"
import ChooseLevelPage from "./pages/choose-level-page.jsx";
import SolveQuestionPage from "./pages/solve-question-page.jsx";
import NewAchievementPage from "./pages/new-achievement-page.jsx";
import ProfilePage from "./pages/profile-page.jsx";

function App() {
  return (
    <>
      <BrowserRouter>
          <Routes>
            <Route path="/" element={<LandingPage/>}/>
            <Route path="/choose-level" element={<ChooseLevelPage/>}/>
            <Route path="/solve-question" element={<SolveQuestionPage/>}/>
            <Route path="/new-achievement" element={<NewAchievementPage/>}/>
            <Route path="/profile" element={<ProfilePage/>}/>
          </Routes>
        </BrowserRouter>
    </>
  )
}

export default App
