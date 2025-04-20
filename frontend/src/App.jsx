import { Outlet } from "react-router-dom";
import Footer from "./components/Footers/Footer";
import Header from "./components/Headers/Header";
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
