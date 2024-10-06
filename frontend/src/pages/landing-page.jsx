import pitLogo from "../assets/pit-logo.svg"
import pitGreeting from "../assets/pit-greeting.png"
import { useNavigate} from "react-router-dom"
import axios from "axios";
import {useInitData} from "@vkruglikov/react-telegram-web-app";
import {useEffect} from "react";

const LandingPage = () => {
  const navigate = useNavigate();
  const [InitDataUnsafe, InitData] = useInitData()

  const handleStart = () => {
    navigate('/choose-level');
  };

  const fetchUser = async () => {
    try {
      await axios.post(
        `${import.meta.env.VITE_REACT_APP_API_URL}/api/v1/users/get-user`, {
        user_init_data: InitData,
      })
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    fetchUser()
  }, [])

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
          <h3>Привет! Я — Пит, твой карманный помощник в изучении Python\</h3>
          <ul className="landing-page__list">
            <li>⭐ 500+ задач разного уровня сложности</li>
            <li>⭐ Новые вопросы каждый день!</li>
            <li>⭐ Получай достижения!</li>
            <li>⭐ Займи первое место в таблице лидеров!</li>
          </ul>
        </p>
        <button onClick={handleStart} className="start-button button">
          Начать 🚀
        </button>
      </div>
    </>
  )
}

export default LandingPage
