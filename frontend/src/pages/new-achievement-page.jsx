import { useNavigate, useLocation} from "react-router-dom"
import {
  MainButton
} from "@vkruglikov/react-telegram-web-app"
import Header from "../components/Header.jsx";
import {useState} from "react"


const NewAchievementPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const achievements = location.state?.achievements;
  const [currentAchievementIndex, setCurrentAchievementIndex] = useState(0);

  const handleMainButtonClick = () => {
    if (currentAchievementIndex < achievements.length - 1) {
      setCurrentAchievementIndex(currentAchievementIndex + 1);
    } else {
      navigate("/solve-question");
    }
  };

  if (achievements.length === 0) {
    navigate("/solve-question");
    return null;
  }

  const currentAchievement = achievements[currentAchievementIndex];
  if (!currentAchievement) {
    navigate("/solve-question");
    return null;
  }

  return (
    <>
      <div className="choose-item">
        <Header title="Python bot" className="header choose-item" />
      </div>
      <div className="landing-page__logo">
        <img className="logo" src={currentAchievement.emoji_image} alt="Achievement Image" />
      </div>
      <div className="landing-page__text">
        <h3>{currentAchievement.title}</h3>
        <p>{currentAchievement.text}</p>
      </div>
      <MainButton
        text={"Забрать достижение! 🎉"}
        onClick={handleMainButtonClick}
      />
    </>
  );
}
export default NewAchievementPage
