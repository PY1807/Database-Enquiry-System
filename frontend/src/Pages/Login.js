import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';
import { AiOutlineEye,AiOutlineEyeInvisible } from "react-icons/ai";
import axios from "axios";
const Login = ({setLoggedIn,setHome,setRegister,setChat,setLogin})=> {
  setLogin(false);
  setRegister(true);
  setChat(true);
    setHome(true);
    const navigate=useNavigate();
    const[form,setform]=useState({username:"",password:""})
    const[showPassword,setPassword]=useState(false)
    function changeHandler(event)
    {
      setform((prevdata)=> (
        {...prevdata,
          [event.target.name]:event.target.value}
      ))
    }
     
    // const endpoint = `http://127.0.0.1:8000/log/`;
     // Django endpoint
    const endpoint=`/log/`
async function postdata() {
  
  const { username, password } = form;
  const data = { username, password };
  try {
    const response = await axios.post(endpoint, data);
    console.log(response.data.message);
    if (response.data.status === "success") {
      toast.success(response.data.message);
      setLoggedIn(true);
      //  // Update state to 
      //  localStorage.setItem('isLoggedIn', 'true');
      navigate("/chat",{state:{username}}); // Redirect to dashboard
      // toast.success("Logged In !!!");
    } else {
      console.log("Ab aayega2")
      toast.error(response.data.message);
  } 
}
  catch (error) {
    console.error("Cannot Logi", error);
    throw error;
  }
}

    async function submitHandler(event)
    {
      console.log("Ha2")
      console.log(typeof(setLoggedIn))
      event.preventDefault();
      console.log("Yes");
        // setLoggedIn(true);
        await postdata();
        
        // navigate("/dashboard")
    }

    return (
     <div>
      <form onSubmit={submitHandler} className="SForm">
      <h1>Login Form</h1>
      <br />
     <h3>Login to your account.</h3>
        <label className="Ut">
          <p>Username</p>
          
          <input required 
          type="text"
          value={form.username}
          onChange={changeHandler}
          name="username"
          placeholder="Enter your email id here"
          />
        </label>

        <label className="Ut">
          <p>Password</p>
          
          <input required 
          type={showPassword?"text":"password"}
          value={form.password}
          onChange={changeHandler}
          name="password"
          placeholder="Enter your password here"
          />
          <span  onClick={()=>setPassword((prev)=> !prev)}>
            {showPassword?(<AiOutlineEye/>):(<AiOutlineEyeInvisible/>)}
          </span>
        </label>
        
        <br />
        <br />
        
        <p onClick={()=> navigate("/forgot")}>
          Forgot Password?
        </p>

       <button className="but" >
        Login
       </button>
         
      </form>
     </div>
    );
  }

export default Login;