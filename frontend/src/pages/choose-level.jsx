import {
  BackButton,
  useInitData,
} from "@vkruglikov/react-telegram-web-app"
import {useNavigate} from "react-router-dom"
import axios from "axios"
import pitGreeting from "../assets/pit-greeting.png";
import {useEffect, useState} from "react"


const ChooseLevel = () => {
  const [InitDataUnsafe, InitData] = useInitData()
  const navigate = useNavigate()
  const [user, setUser] = useState([])

  const fetchUser = async () => {
    try {
      const response = await axios.post(
        `https://493c-147-161-100-131.ngrok-free.app/api/v1/users/get-user`, {
        user_init_data: InitData,
      })
      setUser(response.data)
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    fetchUser()
  }, [])
  return (
    <>
      <BackButton onClick={() => navigate(-1)}/>
      <div className="landing-page__logo">
        <img
          className="logo"
          src={pitGreeting}
          alt="Pit Logo"
        />
      </div>
      {JSON.stringify(user)}
    </>

  )
}

export default ChooseLevel
