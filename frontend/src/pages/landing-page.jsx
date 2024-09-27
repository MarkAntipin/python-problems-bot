import pitLogo from "../assets/pit-logo.svg"
import pitGreeting from "../assets/pit-greeting.png"
import { useNavigate} from "react-router-dom"
import axios from "axios";
import {useInitData, useShowPopup} from "@vkruglikov/react-telegram-web-app";
import {useState, useEffect} from "react";

const LandingPage = () => {
  const navigate = useNavigate();
  const [InitDataUnsafe, InitData] = useInitData()
  const [user, setUser] = useState([])
  const showPopup = useShowPopup()

  const handleStart = () => {
    navigate('/choose-level');
  };

  return (
    <>
      <div className="landing-page">
        <div className="landing-page__logo">
          <img
            className="logo"
            src={pitGreeting}
            alt="Pit Logo"
          />
        </div>
        <p className="landing-page__text">
          <h3>Карманный помощник в изучении Python️</h3>
          <ul className="landing-page__list">
            <li>⭐ 500+ задач разного уровня сложности</li>
            <li>⭐ Новые вопросы каждый день!</li>
            <li>⭐ Получай достижения!</li>
            <li>⭐ Займи первое место в таблице лидеров!</li>
          </ul>
        </p>
        <button onClick={handleStart} className="start-button button">
          Начать 🚀
          <span>
            <img src={pitLogo} alt="Start" />
          </span>
        </button>
      </div>
    </>
  )
}

export default LandingPage
