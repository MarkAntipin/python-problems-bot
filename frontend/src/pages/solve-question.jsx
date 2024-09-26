import ReactMarkdown from 'react-markdown';
import {useEffect, useState} from "react"
import {
  BackButton,
  MainButton,
  useCloudStorage,
  useHapticFeedback,
  useShowPopup
} from "@vkruglikov/react-telegram-web-app";
import {useNavigate} from "react-router-dom"
import Header from "../components/Header.jsx"
import CodeBlock from "../components/CodeBlock.jsx";
import AnswerItem from "../components/AnswerlItem.jsx";
import ExplanationBlock from "../components/ExplanationBlock.jsx";

const SolveQuestion = () => {
  const navigate = useNavigate()
  const storage = useCloudStorage()
  const showPopup = useShowPopup()
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [impactOccurred, notificationOccurred, selectionChanged] = useHapticFeedback()
  const [showExplanation, setShowExplanation] = useState(false);


  const codeString = `
import logging
handler = logging.FileHandler('myapp.log')
formatter = logging.Formatter(
  '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
 )
handler.setFormatter(formatter)
`;
  const question = "## Что делает следующий код?"
  const explanation = "Этот код создает обработчик `FileHandler` для записи логов в файл `myapp.log` и настраивает его с помощью заданного форматтера, который определяет формат логов\\."
  const explanationTitle = "Браво! Совершенно верно! 🤝"
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
    setShowExplanation(true);
  };

  const handleMainButtonClickAfterExplanation = async () => {
    navigate('/new-achievement');
  };

  useEffect(() => {
  }, []);


  return (
    <>
      {/*точно нужно?*/}
      <BackButton onClick={() => navigate(-1)}/>
      {/*точно нужно?*/}
      <div className="choose-item">
      <Header title="Python bot" className="header choose-item"/>
          <ReactMarkdown>
            {question}
          </ReactMarkdown>
          <CodeBlock
            codeString={codeString}
          >
          </CodeBlock>
        {!showExplanation ? (
          <main className="main_answer">
            <AnswerItem
              answerText="Создает обработчик, который записывает логи в файл без форматирования"
              onClick={() => handleAnswerClick('A')}
              className={selectedAnswer === 'A' ? "answer_item answer_item--active" : "answer_item"}
            >
            </AnswerItem>
            <AnswerItem
              answerText="Настройка форматирования логов будет проигнорирована"
              onClick={() => handleAnswerClick('B')}
              className={selectedAnswer === 'B' ? "answer_item answer_item--active" : "answer_item"}
            >
            </AnswerItem>
            <AnswerItem
              answerText="Создает и настраивает обработчик для записи логов в файл `myapp.log` с заданным форматированием"
              onClick={() => handleAnswerClick('C')}
              className={selectedAnswer === 'C' ? "answer_item answer_item--active" : "answer_item"}
            >
            </AnswerItem>
            <AnswerItem
              answerText="Генерирует ошибку из-за неправильного использования `Formatter`"
              onClick={() => handleAnswerClick('D')}
              className={selectedAnswer === 'D' ? "answer_item answer_item--active" : "answer_item"}
            >
            </AnswerItem>
          </main>
          ) : (
          <ExplanationBlock
            explanation={explanation}
            title={correctExplanationTitles[randomCorrectExplanationTitle]}
            userAnswer="Создает и настраивает обработчик для записи логов в файл `myapp.log` с заданным форматированием"
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

export default SolveQuestion
