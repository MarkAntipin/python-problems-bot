import pitLogo from "../assets/pit-logo.svg"

const Header = ({title, className}) => {
  return (
    <header className={`${className}__header`}>
      <div className="top-bar">
        <p className="top-bar__text">{title}</p>
        <div className="top-bar__icon">
          <img
            className="top-bar__icon__img--about"
            src={pitLogo}
            alt="Button"
          />
        </div>
      </div>
    </header>
  )
}


export default Header
