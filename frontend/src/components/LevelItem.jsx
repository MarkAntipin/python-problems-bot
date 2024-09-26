const LevelItem = ({
  title, description, levelImage,
  onClick, className
}) => (
  <section className={className} onClick={onClick}>
    <div className="level_item__image">
      <img
        className="level_item__image__img"
        src={levelImage}
        alt="Level"
      />
    </div>

    <div className="level_item__info">
      <h1 className="level_item__title">{title}</h1>
      <p className="level_item__description">{description}</p>
    </div>
  </section>
)

export default LevelItem
