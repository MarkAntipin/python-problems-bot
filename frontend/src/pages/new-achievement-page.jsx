import moonImage from "../assets/moon.svg"
import { useNavigate} from "react-router-dom"
import {
  BackButton,
  MainButton
} from "@vkruglikov/react-telegram-web-app"
import Header from "../components/Header.jsx";


const NewAchievementPage = () => {
  const navigate = useNavigate();
  // const

  return (
    <>
      {/*точно нужно?*/}
      <BackButton onClick={() => navigate(-1)}/>
      {/*точно нужно?*/}
      <div className="choose-item">
      <Header title="Python bot" className="header choose-item"/>
      </div>
      <div className="landing-page__logo">
        <img
          className="logo"
          src={moonImage}
          alt="Achievement Image"
        />
      </div>
      <p className="landing-page__text">
        <h3>Король Конфузов</h3>
        50 неправильно решенных задач
      </p>
      <
      MainButton
        text={"Забрать достижение! 🎉"}
      />
    </>
  );
}
export default NewAchievementPage
