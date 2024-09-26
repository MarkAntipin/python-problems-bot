import pitLogo from "../assets/pit-logo.svg"
import moonImage from "../assets/moon.svg"
import { useNavigate} from "react-router-dom"
import {
  BackButton,
  useInitData,
  useShowPopup,
  useHapticFeedback,
  useCloudStorage,
  MainButton
} from "@vkruglikov/react-telegram-web-app"
import Header from "../components/Header.jsx";
import LevelItem from "../components/LevelItem.jsx";
import kidImage from "../assets/kid.svg";
import graduatedImage from "../assets/graduated.svg";
import programmerImage from "../assets/programmer.svg";
import ReactMarkdown from "react-markdown";
import CodeBlock from "../components/CodeBlock.jsx";
import AnswerItem from "../components/AnswerlItem.jsx";
import ExplanationBlock from "../components/ExplanationBlock.jsx";


const NewAchievementPage = () => {
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
