import React from "react";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import Chatroom from "./Chatroom";

const Chat = ({isLoggedIn,setHome,setChat,setLogin,setNav,setusername}) => {
  setLogin(true);
  setHome(true);
  setChat(false);
  const navigate=useNavigate();
 const location=useLocation();
 const {username}=location.state || {};
 
 setusername(username);
  useEffect(() => {
    if (!isLoggedIn) {
      const timer = setTimeout(() => {
        navigate('/login');
      }, 3000);

      return () => clearTimeout(timer); // Cleanup the timer if the component unmounts
    }
  }, []);
  return (
     <div>
      {
         !isLoggedIn && <h1>You haven't logged in yet</h1>
      }

      {
        
        
        // <h2>Yes yes yes ...</h2> 
        isLoggedIn && <Chatroom username={username}/>
     
      }
       
     </div>
  );
}

export default Chat;