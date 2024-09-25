import {Prism as SyntaxHighlighter} from "react-syntax-highlighter";

const CodeBlock = ({ codeString }) => (
  <div className="code-block">
      <SyntaxHighlighter language="python">
        {codeString}
      </SyntaxHighlighter>
  </div>
)

export default CodeBlock
