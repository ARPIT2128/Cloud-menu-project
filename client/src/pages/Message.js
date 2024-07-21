import DockerfileGenerator from "../components/Docker_hindi";
import Gemini from "../components/Gemini";

function Message(params) {
  return (
    <>
      <div>
        <Gemini />
      </div>
      <div style={{ marginTop: "40px" }}>
        <DockerfileGenerator />
      </div>
    </>
  );
}

export default Message;
