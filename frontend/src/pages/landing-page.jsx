import pitLogo from "../assets/pit-logo.svg"
import pitGreeting from "../assets/pit-greeting.png"
import {Link} from "react-router-dom"

const LandingPage = () => {
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
          Привет! Я — Пит, твой карманный помощник в изучении Python и подготовке к собеседованиям.
          🔹 Выбирай уровень сложности вопросов — от новичка до опытного разработчика
          🔹 Бот каждый день будет присылать 3 вопроса. Это займет всего 5-10 минут в день!
          🔹 Зарабатывай достижения и соревнуйся с другими пользователями
        </p>
        <Link to="/choose-level" className="arrow-button button">Начать 🚀
          <span className="arrow">
            <img src={pitLogo} alt="Arrow Right"/>
          </span>
        </Link>
      </div>
    </>
  )
}

export default LandingPage
