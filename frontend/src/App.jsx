import { Outlet } from "react-router-dom";
import Header from "./components/header/Header";
import { Footer } from "./components/footer/Footer";
import "./global.css";

function App() {
  return (
    <>
      <Header />
      <main>
        <Outlet></Outlet>
      </main>
      <Footer />
    </>
  );
}

export default App;
