
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import  Signup from "./components/common/Signup" ;
// import { UserSidebar } from "./components/layouts/UserSidebar";
import { Login } from "./components/common/Login";
import axios from "axios";
import Home from "./components/common/Home";
import UserNavbar from "./components/layouts/UserNavbar";
import CarSearch from "./components/common/CarSearch";
// import { UserNavbar } from "./components/layouts/UserNavbar";

const App = () => {
  axios.defaults.baseURL = "http://localhost:8000"; // Set the base URL for all requestsa
  return (
    <Router>
       <UserNavbar/>
        <div className="container">
          <Routes>
          {/* <Route path="/" element={<UserNavbar></UserNavbar>} /> */}
            <Route path = "/" element={<Home/>} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup></Signup>} />
            <Route path="/search" element={<CarSearch></CarSearch>}/>
         
          </Routes>
        </div>
       </Router>
   
  );
};

export default App;
