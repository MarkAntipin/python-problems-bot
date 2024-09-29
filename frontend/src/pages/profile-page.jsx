import {useInitData} from "@vkruglikov/react-telegram-web-app";

const ProfilePage = () => {
  const [InitDataUnsafe, InitData] = useInitData()

  return (
    <>
      {InitDataUnsafe.user.first_name}
    </>
  )
}

export default ProfilePage
