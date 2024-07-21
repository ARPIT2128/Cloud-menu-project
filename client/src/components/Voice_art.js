// import React, { useState } from "react";\

// import axios from "axios";

// const VoiceArt = () => {
//   const [audioDetails, setAudioDetails] = useState({
//     url: "",
//     blob: null,
//     chunks: [],
//     duration: { h: 0, m: 0, s: 0 },
//   });
//   const [coverArt, setCoverArt] = useState("");

//   const handleAudioStop = (data) => {
//     setAudioDetails(data);
//   };

//   const handleAudioUpload = async () => {
//     const formData = new FormData();
//     formData.append("audio", audioDetails.blob, "audio.wav");

//     try {
//       const response = await axios.post(
//         "http://localhost:8080/generate_cover_art",
//         formData,
//         {
//           headers: {
//             "Content-Type": "multipart/form-data",
//           },
//         }
//       );
//       const imageBlob = response.data;
//       const imageObjectURL = URL.createObjectURL(
//         new Blob([imageBlob], { type: "image/png" })
//       );
//       setCoverArt(imageObjectURL);
//     } catch (error) {
//       console.error("Error generating cover art:", error);
//     }
//   };

//   return (
//     <div>
//       <h1>Cover Art Generator</h1>
//       <Recorder
//         record={true}
//         title={"New Recording"}
//         audioURL={audioDetails.url}
//         showUIAudio
//         handleAudioStop={handleAudioStop}
//         handleAudioUpload={handleAudioUpload}
//         handleReset={() =>
//           setAudioDetails({
//             url: "",
//             blob: null,
//             chunks: [],
//             duration: { h: 0, m: 0, s: 0 },
//           })
//         }
//       />
//       {audioDetails.url && (
//         <div>
//           <h2>Recorded Audio:</h2>
//           <audio src={audioDetails.url} controls="controls" />
//         </div>
//       )}
//       {coverArt && (
//         <div>
//           <h2>Generated Cover Art:</h2>
//           <img src={coverArt} alt="Generated Cover Art" />
//         </div>
//       )}
//     </div>
//   );
// };

// export default VoiceArt;
