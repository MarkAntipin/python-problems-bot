import ReactMarkdown from "react-markdown";

const ExplanationBlock = ({ explanation, title, correctAnswer, userAnswer }) => (
  <div className="explanation-block">
    <div className="explanation-block__title">
      <ReactMarkdown>{title}</ReactMarkdown>
    </div>
      <ReactMarkdown>
        ## Твой ответ:
      </ReactMarkdown>

      <div className="explanation-block__text">
        <ReactMarkdown>
          {userAnswer}
        </ReactMarkdown>
      </div>

      <ReactMarkdown>
        ## Объяснение:
      </ReactMarkdown>
      <ReactMarkdown className="explanation-block__text">
        {explanation}
      </ReactMarkdown>
  </div>
)

export default ExplanationBlock
