import {
  BackButton,
  useInitData,
  useShowPopup,
  useHapticFeedback,
  useCloudStorage,
  MainButton
} from "@vkruglikov/react-telegram-web-app"
import {useNavigate} from "react-router-dom"
import axios from "axios"
import {useState} from "react"
import Header from "../components/Header.jsx"
import LevelItem from "../components/LevelItem.jsx";
import kidImage from "../assets/kid.svg"
import graduatedImage from "../assets/graduated.svg"
import programmerImage from "../assets/programmer.svg"



const ChooseLevel = () => {
  const [InitDataUnsafe, InitData] = useInitData()
  const storage = useCloudStorage()
  const navigate = useNavigate()
  const [user, setUser] = useState([])
  const showPopup = useShowPopup()
  const [selectedLevelId, setSelectedLevelId] = useState(null)
  const [impactOccurred, notificationOccurred, selectionChanged] = useHapticFeedback()

  const fetchUser = async () => {
    const url = 'http://0.0.0.0:3779'
    try {
      const response = await axios.post(
        `${url}/api/v1/users/get-user`, {
        user_init_data: InitData,
      })
      setUser(response.data)
    } catch (err) {
      console.error(err)
    }
  }

  const handleLevelClick = async (level_id) => {
    if (selectedLevelId === level_id) {
      setSelectedLevelId(null)
      selectionChanged()
      await storage.removeItem("selectedLevelId")
      return
    } else if (selectedLevelId) {
      setSelectedLevelId(level_id)
      selectionChanged()
    } else {
      setSelectedLevelId(level_id)
      notificationOccurred("success")
    }
  }

  // useEffect(() => {
  //   fetchUser()
  // }, [])
  return (
    <>
      <BackButton onClick={() => navigate(-1)}/>
      <div className="choose-item">
        <Header title="Выбери уровень" className="header choose-item"/>
        <main className="main">
          <LevelItem
            className={selectedLevelId === 1 ? "level_item level_item--active" : "level_item"}
            title="Новичок"
            description="Я новичок, прошел переменные, циклы и условия в Python"
            levelImage={kidImage}
            onClick={() => handleLevelClick(1)}
          />
          <LevelItem
            className={selectedLevelId === 2 ? "level_item level_item--active" : "level_item"}
            title="Хочу хитрые задачи"
            description="Я уже много знаю, хочу задачи на глубину языка Python"
            levelImage={graduatedImage}
            onClick={() => handleLevelClick(2)}
          />
          <LevelItem
            className={selectedLevelId === 3 ? "level_item level_item--active" : "level_item"}
            title="Программист"
            description="Я хочу узнать больше про возможности python и связанные с ним технологии"
            levelImage={programmerImage}
            onClick={() => handleLevelClick(3)}
          />
        </main>
    </div>
    {selectedLevelId && <
      MainButton
        text={`Выбран уровень ${selectedLevelId}`}
        onClick={async () => navigate('/solve-question')}
    />}
    </>
  )
}

export default ChooseLevel
