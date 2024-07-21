import Audio_text from "../components/Audio_text";
import MicrophoneAccess from "../components/Microphone";
import CoverArtGenerator from "../components/Voice_art";
function Audio() {
  return (
    <>
      <div className="card-container">
        <MicrophoneAccess />
      </div>
      <div className="card-container">
        <Audio_text />
      </div>
    </>
  );
}

export default Audio;
