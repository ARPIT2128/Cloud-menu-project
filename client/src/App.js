import Navbar from "./components/Navbar";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";

import Home from "./pages/Home";
import Vision from "./pages/Vision";
import AWS from "./pages/AWS";
import Audio from "./pages/Audio";
import Message from "./pages/Message";

function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: (
        <>
          <Navbar />
          <Home />
        </>
      ),
    },
    {
      path: "/Vision",
      element: (
        <>
          <Navbar />
          <Vision />
        </>
      ),
    },
    {
      path: "/AWS",
      element: (
        <>
          <Navbar />
          <AWS />
        </>
      ),
    },
    {
      path: "/Audio",
      element: (
        <>
          <Navbar />
          <Audio />
        </>
      ),
    },
    {
      path: "/Message",
      element: (
        <>
          <Navbar />
          <Message />
        </>
      ),
    },
  ]);
  return (
    <div className="App">
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
