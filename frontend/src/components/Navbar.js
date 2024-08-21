import React from "react";
import logo from "../logo.svg"
import './Navbar.css'
import { Link} from "react-router-dom";
import axios from "axios";

import { toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';

const Navbar = (props) => {
  const isLoggedIn=props.isLoggedIn;
  const isRegister=props.isRegister;
  const isHome=props.isHome;
  const isChat=props.isChat;
  const isLogin=props.isLogin;
  const setLogin=props.setLogin;
  const setChat=props.setChat;
  const setHome=props.setHome;
  const username=props.username;
  const setRegister=props.setRegister;
  const setLoggedIn=props.setLoggedIn;
  
  setHome(true);
  setRegister(true);
  setLogin(true);
  setChat(true);

  async function submithandler()
   {
    setLoggedIn(false);
    const response = await axios.post('/logout/',{username})
    
    sessionStorage.removeItem('isLoggedIn');
    sessionStorage.removeItem('username');
    toast.success("Logged Out successfully.")
    // localStorage.removeItem('isLoggedIn');
   }

  return (

    <div className="Nav">
  
    
    <img src={logo} alt="image"  width={160} height={70} loading="lazy"/>
    

    <nav className="Ele">
     {isHome && <ol  >
        <li>
          <Link to="/" >
          <button className="Buttons">
          Home
          </button>
         
          </Link>
          
        </li>
      </ol> 
}
      
    </nav>
    <div className="Button">
      {
        isLogin && !isLoggedIn &&
        <Link to="/login">
          <button className="Buttons">
            Login
          </button>
        </Link>
      }
      {
       isRegister && !isLoggedIn &&
        <Link to="/signup">
          <button className="Buttons" >
            Register
          </button>
        </Link>
      }
      {
       isChat && !isLoggedIn &&
        <Link to="/chat">
          <button className="Buttons">
            Start Chat
          </button>
        </Link>
      }
      {
        isLoggedIn &&
        <Link to="/">
          <button className="Buttons" onClick={submithandler}>
            Logout
          </button>
        </Link>
      }
    </div>
  </div>
  );
  
}

export default Navbar;