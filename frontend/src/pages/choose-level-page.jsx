import {
  BackButton,
  useInitData,
  useHapticFeedback,
  useCloudStorage,
  MainButton
} from "@vkruglikov/react-telegram-web-app"
import {useNavigate} from "react-router-dom"
import axios from "axios"
import {useState, useEffect} from "react"
import Header from "../components/Header.jsx"
import LevelItem from "../components/LevelItem.jsx";
import kidImage from "../assets/kid.svg"
import graduatedImage from "../assets/graduated.svg"
import programmerImage from "../assets/programmer.svg"



const ChooseLevelPage = () => {
  const [InitDataUnsafe, InitData] = useInitData()
  const storage = useCloudStorage()
  const navigate = useNavigate()
  const [selectedLevel, setSelectedLevel] = useState(null)
  const [impactOccurred, notificationOccurred, selectionChanged] = useHapticFeedback()

  const setUserLevel = async (levelId) => {
    try {
      await axios.post(
        `${import.meta.env.VITE_REACT_APP_API_URL}/api/v1/users/set-level`, {
        user_init_data: InitData,
        level: levelId
      })
    } catch (err) {
      console.error(err)
    }
  }

  const handleLevelClick = async (level) => {
    const isSameLevelSelected = level.id === selectedLevel?.location_id

    if (isSameLevelSelected) {
      setSelectedLevel(null)
      selectionChanged()
      await storage.removeItem("selectedLevel")
      return
    } else if (selectedLevel) {
      setSelectedLevel(level)
      selectionChanged()
    } else {
      setSelectedLevel(level)
      notificationOccurred("success")
    }
  }
  const handleMainButtonClick = async () => {
    await setUserLevel(selectedLevel.id)
    navigate('/solve-question')
  };

  return (
    <>
      <BackButton onClick={() => navigate(-1)}/>
      <div className="choose-item">
        <Header title="Выбери уровень" className="header choose-item"/>
        <main className="main">
          <LevelItem
            className={selectedLevel && selectedLevel.id === 1 ? "level_item level_item--active" : "level_item"}
            title="Новичок"
            description="Я новичок, прошел переменные, циклы и условия в Python"
            levelImage={kidImage}
            onClick={() => handleLevelClick({"id": 1, "name": "Новичок"})}
          />
          <LevelItem
            className={selectedLevel && selectedLevel.id === 2 ? "level_item level_item--active" : "level_item"}
            title="Хочу хитрые задачи"
            description="Я уже много знаю, хочу задачи на глубину языка Python"
            levelImage={graduatedImage}
            onClick={() => handleLevelClick({"id": 2, "name": "Хочу хитрые задачи"})}
          />
          <LevelItem
            className={selectedLevel && selectedLevel.id === 3 ? "level_item level_item--active" : "level_item"}
            title="Программист"
            description="Я хочу узнать больше про возможности python и связанные с ним технологии"
            levelImage={programmerImage}
            onClick={() => handleLevelClick({"id": 3, "name": "Программист"})}
          />
        </main>
    </div>
    {selectedLevel && <
      MainButton
        text={`Выбрать уровень: ${selectedLevel.name}`}
        onClick={async () => handleMainButtonClick()}
    />}
    </>
  )
}

export default ChooseLevelPage
