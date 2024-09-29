import axeImage from "../assets/axe.svg"
import blinImage from "../assets/blin.svg"
import brainImage from "../assets/brain.svg"
import graduatedImage from "../assets/graduated.svg"
import guitarImage from "../assets/guitar.svg"
import infinityImage from "../assets/infinity.svg"
import ironImage from "../assets/iron.svg"
import kidImage from "../assets/kid.svg"
import marafonImage from "../assets/marafon.svg"
import medalImage from "../assets/medal.svg"
import moonImage from "../assets/moon.svg"
import musicImage from "../assets/music.svg"
import ninjaImage from "../assets/ninja.svg"
import programmerImage from "../assets/programmer.svg"
import rocketImage from "../assets/rocket.svg"
import scienceImage from "../assets/science.svg"
import seniorImage from "../assets/senior.svg"
import targetImage from "../assets/target.svg"

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
  const emojiKeyToImage = {
    "axe": axeImage,
    "blin": blinImage,
    "brain": brainImage,
    "graduated": graduatedImage,
    "guitar": guitarImage,
    "infinity": infinityImage,
    "iron": ironImage,
    "kid": kidImage,
    "marafon": marafonImage,
    "medal": medalImage,
    "moon": moonImage,
    "music": musicImage,
    "ninja": ninjaImage,
    "programmer": programmerImage,
    "rocket": rocketImage,
    "science": scienceImage,
    "senior": seniorImage,
    "target": targetImage,
  }


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
        <img className="logo" src={emojiKeyToImage[currentAchievement.emoji_key]} alt="Achievement Image" />
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
