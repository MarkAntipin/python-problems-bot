import {
  BackButton,
  MainButton,
  useInitData,
} from "@vkruglikov/react-telegram-web-app"
import {Link, useNavigate, useParams} from "react-router-dom"
import axios from "axios"
import pitGreeting from "../assets/pit-greeting.png";
import fs from 'fs/promises';
import {useEffect, useState} from "react"
import {BrowserRouter, Route, Routes} from "react-router-dom"
import pitLogo from "../assets/pit-logo.svg";


const ChooseLevel = () => {
  const webApp = window.Telegram?.WebApp
  const [InitDataUnsafe, InitData] = useInitData()
  const navigate = useNavigate()
  const [user, setUser] = useState([])



  const fetchUser = async () => {
    // https://02e6-147-161-100-131.ngrok-free.app/api/v1/users
    try {
      const params = {user_init_data: InitData};
      const response = await axios.get(
        `http://localhost:8000/api/v1/users`, {
        params: params,
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
      {user}
    </>
  )
}

export default ChooseLevel

