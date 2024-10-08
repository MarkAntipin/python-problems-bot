import ReactMarkdown from 'react-markdown';
import {useEffect, useState} from "react"
import {
  MainButton,
  useCloudStorage,
  useHapticFeedback, useInitData,
} from "@vkruglikov/react-telegram-web-app";
import {useNavigate} from "react-router-dom"
import Header from "../components/Header.jsx"
import CodeBlock from "../components/CodeBlock.jsx";
import AnswerItem from "../components/AnswerlItem.jsx";
import ExplanationBlock from "../components/ExplanationBlock.jsx";
import axios from "axios";
import pitGreeting from "../assets/pit-greeting.png";
import aboutToCry from "../assets/about-to-cry.svg";


const correctExplanationTitles = [
  "Браво! Совершенно верно! 🤝",
  "И это правильный ответ! ✅",
  "Точно в яблочко! 🎯",
  "Ура, это правильный ответ! 🎉",
  "Верно! Ты просто космос! 🚀",
  "Правильный ответ! 👍",
  "Так точно! Ты справился на ура! 🏆",
  "Верно! У тебя отлично получается! 😉",
  "Да, это правильный ответ! 👌",
  "Абсолютно верно! 🌟"
]
const randomCorrectExplanationTitle = Math.floor(Math.random() * correctExplanationTitles.length);

const incorrectExplanationTitles = [
  "Ой-ой, кажется, это не тот ответ 😯",
  "Упс, мимо! 🙊",
  "Ошибочка вышла 🙈",
  "Не угадал! 🙅‍️",
  "К сожалению, это не так 🚫",
  "Не тот ответ, друг 🕵️‍♂️"
]
const randomIncorrectExplanationTitle = Math.floor(Math.random() * incorrectExplanationTitles.length);

const enoughQuestionsForTodayTexts = [
  `Сегодня – всё! Жди новых заданий на пути к изучению Python уже завтра⚡️
  Ты можешь дальше-больше! Камон, эврибади пучехензап 💥`,
  `«Для средульки хватит!» Новые задачки уже завтра⚡️`,
  `На сегодня всё! Задачи ждут тебя завтра, а пока отдыхай и набирайся сил 🔋`,
  `Белиссимо 🤌 Завтра жди новые крутые задачи!`,
  `Ты молодец🌟 Завтра встречаемся как обычно!`,
  `Сегодня все! С нетерпением жду тебя завтра👋`,
  `На сегодня все, отдыхай! А я уже готовлю для тебя новые задачи на завтра 🤩`
];
const randomEnoughQuestionsForTodayText = Math.floor(Math.random() * enoughQuestionsForTodayTexts.length);


const SolveQuestionPage = () => {
  const navigate = useNavigate()
  const storage = useCloudStorage()
  const [InitDataUnsafe, InitData] = useInitData()
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [impactOccurred, notificationOccurred, selectionChanged] = useHapticFeedback()
  const [showExplanation, setShowExplanation] = useState(false);
  const [newQuestion, setNewQuestion] = useState(null)
  const [noMoreQuestion, setNoMoreQuestion] = useState(false)
  const [needPayment, setNeedPayment] = useState(false)
  const [loading, setLoading] = useState(true);
  const [userAnswer, setUserAnswer] = useState(null)

  const fetchNewQuestion = async () => {
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_REACT_APP_API_URL}/api/v1/questions/get-new-question`, {
        user_init_data: InitData,
      })
      setNewQuestion(response.data)
    } catch (err) {
      if (err.response) {
        if (err.response.status === 400) {
          setNoMoreQuestion(true)
        } else if (err.response.status === 402) {
          setNeedPayment(true)
        } else {
          console.error(err)
        }
      }
    } finally {
      setLoading(false);
    }
  }

  const answerQuestion = async (questionId, answer) => {
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_REACT_APP_API_URL}/api/v1/questions/answer`, {
        user_init_data: InitData,
        question_id: questionId,
        user_answer: answer
      })
      setUserAnswer(response.data)
    } catch (err) {
      console.error(err)
    }
  }

  const sendPayment = async () => {
    try {
      await axios.post(
        `${import.meta.env.VITE_REACT_APP_API_URL}/api/v1/payment/send-payment`, {
        user_init_data: InitData,
      })
    } catch (err) {
      console.error(err)
    }
  }

  const handleAnswerClick = async (answer) => {
    if (selectedAnswer === answer) {
      setSelectedAnswer(null)
      selectionChanged()
      await storage.removeItem("selectedAnswer")
      return
    } else if (selectedAnswer) {
      setSelectedAnswer(answer)
      selectionChanged()
    } else {
      setSelectedAnswer(answer)
      notificationOccurred("success")
    }
  }

  const handleMainButtonClick = async () => {
    await answerQuestion(newQuestion.id, selectedAnswer)
    setShowExplanation(true);
  };

  const handleMainButtonClickAfterExplanation = async () => {
    setSelectedAnswer(null)
    if (userAnswer?.achievements && userAnswer.achievements.length > 0) {
      navigate('/new-achievement', { state: { achievements: userAnswer.achievements } });
    } else {
      window.location.reload()
    }
  };

  const handlePaymentButtonClick = async () => {
    await sendPayment()
    window.Telegram.WebApp.close()
  };

  const handleToProfile = () => {
    navigate('/profile');
  };

  useEffect(() => {
    fetchNewQuestion()
  }, [])

  if (loading) {
    return (
      <>
        <div className="landing-page">
          <p className="landing-page__text">Загрузка...⏳</p>
        </div>
      </>
    )
  }

  if (noMoreQuestion) {
    return (
      <div className="landing-page">
      <Header title="Python bot" className="header choose-item"/>

        <div className="landing-page__logo">
          <img
            className="logo"
            src={pitGreeting}
            alt="Pit Logo"
          />
        </div>
        <p className="landing-page__text">
          {enoughQuestionsForTodayTexts[randomEnoughQuestionsForTodayText]}
        </p>
        <button onClick={handleToProfile} className="start-button button">
          Посмотреть мои достижения 🏆
        </button>
      </div>
    );
  }

  if (needPayment) {
    return (
      <div className="landing-page">
      <Header title="Python bot" className="header choose-item"/>

        <div className="landing-page__logo">
          <img
            className="logo"
            src={aboutToCry}
            alt="Payment logo"
          />
        </div>
        <p className="landing-page__text">
          Твой бесплатный период закончился!
          Всего за 799 рублей ты получишь:
          <ul className="landing-page__list">
            <li>⭐ 500+ задач разного уровня сложности</li>
            <li>⭐ Новые вопросы и достижения!</li>
            <li>⭐ Подборки по слабым темам!</li>
          </ul>
          Я стараюсь развивать проект и добавлять новые фишки, и твоя поддержка мне очень поможет!
        </p>
        <button onClick={handlePaymentButtonClick} className="start-button button">
          Оплатить
        </button>
      </div>
    );
  }

  return (
    <>
      <div className="choose-item">
      <Header title="Python bot" className="header choose-item"/>
          <ReactMarkdown>
            {`## ${newQuestion.question_text}`}
          </ReactMarkdown>
          {newQuestion.code_block && (
            <CodeBlock
              codeString={newQuestion.code_block}
            >
            </CodeBlock>
          )}

        {!showExplanation ? (
          <main className="main_answer">
              {Object.entries(newQuestion.choices).map(([key, value]) => (
                <AnswerItem
                  key={key}
                  answerText={value}
                  onClick={() => handleAnswerClick(key)}
                  className={selectedAnswer === key ? "answer_item answer_item--active" : "answer_item"}
                >
                </AnswerItem>
              ))}
          </main>
          ) : (
            <ExplanationBlock
              explanation={newQuestion.explanation}
              correctTitle={correctExplanationTitles[randomCorrectExplanationTitle]}
              incorrectTitle={incorrectExplanationTitles[randomIncorrectExplanationTitle]}
              userAnswer={newQuestion.choices[selectedAnswer]}
              correctAnswer={newQuestion.choices[newQuestion.answer]}
              isCorrect={userAnswer.is_correct}
            >
            </ExplanationBlock>
          )
        }
      </div>

        {selectedAnswer && (
          <MainButton
            text={showExplanation ? "Далее" : `Ответить ${selectedAnswer}`}
            onClick={showExplanation ? handleMainButtonClickAfterExplanation : handleMainButtonClick}
          />
        )}
    </>
  );
}

export default SolveQuestionPage
