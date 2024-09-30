import ReactMarkdown from "react-markdown";

const ExplanationBlock = ({explanation, correctTitle, incorrectTitle, correctAnswer, userAnswer , isCorrect}) => (
  <div className="explanation-block">
    {/* Title */}
    <div className="explanation-block__title">
      <ReactMarkdown>{isCorrect ? correctTitle : incorrectTitle}</ReactMarkdown>
    </div>

    {/* User's answer */}
    <ReactMarkdown>
      ## Твой ответ:
    </ReactMarkdown>
    <div className="explanation-block__text">
      <ReactMarkdown>
        {userAnswer}
      </ReactMarkdown>
    </div>

    {/* Correct answer (only if isCorrect is false) */}
    {!isCorrect && (
      <>
        <ReactMarkdown>
          ## Правильный ответ:
        </ReactMarkdown>
        <div className="explanation-block__text">
          <ReactMarkdown>
            {correctAnswer}
          </ReactMarkdown>
        </div>
      </>
    )}

    {/* Explanation */}
    <ReactMarkdown>
      ## Объяснение:
    </ReactMarkdown>
    <div className="explanation-block__text">
      <ReactMarkdown>
        {explanation}
      </ReactMarkdown>
    </div>
  </div>
)

export default ExplanationBlock
