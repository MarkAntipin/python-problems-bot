import pitLogo from "../assets/pit-logo.svg"
import pitGreeting from "../assets/pit-greeting.png"
import { useNavigate} from "react-router-dom"

const LandingPage = () => {
  const navigate = useNavigate();

  const handleStart = () => {
    // const condition = false;
    const condition = true;

    if (condition) {
      navigate('/choose-level');
    } else {
      navigate('/solve-question');
    }
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
