import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useInitData } from '@vkruglikov/react-telegram-web-app';
import Header from "../components/Header.jsx";

const ProfilePage = () => {
  const [InitDataUnsafe, InitData] = useInitData();
  const [userProfile, setUserProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchUserProfile = async () => {
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_REACT_APP_API_URL}/api/v1/users/get-user-profile`,
        {
          user_init_data: InitData,
        }
      );
      setUserProfile(response.data);
      setLoading(false);
    } catch (err) {
      console.error("Error fetching user profile:", err);
      setError(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    if (InitData) {
      fetchUserProfile();
    }
  }, [InitData]);

  if (loading) {
    return <div>Загрузка...</div>;
  }

  if (error) {
    return <div>Ошибка при загрузке профиля: {error.message}</div>;
  }

  if (!userProfile) {
    return <div>Нет данных профиля.</div>;
  }

  return (
    <>
      <div className="choose-item">
        {InitDataUnsafe.user && (
          <Header title={userProfile.username} className="header choose-item" />
        )}
        {InitDataUnsafe.user.photo_url && (
          <div className="landing-page__logo">
            <img
              src={InitDataUnsafe.user.photo_url}
              className="avatar"
            />
          </div>
        )}
        <div className="landing-page__text">
          <h3>Твоё место в рейтинге: {userProfile.user_position}</h3>
          <h3>Достижения:</h3>
          {userProfile.achievements && userProfile.achievements.length > 0 ? (
            <div className="landing-page__list">
              <ul>
                {userProfile.achievements.map((achievement, index) => (
                  <li key={index}>
                    {achievement.emoji} {achievement.text} - {achievement.title}
                  </li>
                ))}
              </ul>
              <p>{userProfile.achievements_statistic}</p>
            </div>
          ) : (
            <div>У тебя пока нет достижений (</div>
          )}
        </div>
      </div>
    </>
  );
};

export default ProfilePage;
