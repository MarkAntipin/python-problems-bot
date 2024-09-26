import ReactMarkdown from 'react-markdown';

const AnswerItem = ({
  answerText,
  onClick, className
}) => (
  <section className={className} onClick={onClick}>
    <ReactMarkdown className="answer_item__text">
      {answerText}
    </ReactMarkdown>
  </section>
)

export default AnswerItem
