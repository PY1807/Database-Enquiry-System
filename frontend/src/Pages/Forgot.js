import React, { useState } from "react";
import { AiOutlineEye,AiOutlineEyeInvisible } from "react-icons/ai";
import axios from "axios";
import { toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from "react-router-dom";

const Forgot = ({setotpsent}) => {

  console.log("YEs Yes Yes");
  
 
  const[form,setform]=useState({username:"",email:""})
    function changeHandler(event)
    {
      setform((prevdata)=> (
        {...prevdata,
          [event.target.name]:event.target.value}
      ))
    }
  
  
  const navigate=useNavigate();
  // const endpoint = `http://127.0.0.1:8000/otp/`; // Django endpoint http://localhost:8080
  const endpoint = `/otp/`;
async function postdata() {
  console.log("aa gaye post data ke andar")
  
  const {username,email}=form
  const data = {username,email};
  try {
    const response = await axios.post(endpoint, data);
    console.log(response.data.status)
    if (response.data.status === "success") {
      console.log("success")
      
      toast.success('Otp sent')
      setotpsent(true);
      const otp_to_check=response.data.otp_to_check
      navigate("/otp1",{ state: { username,email,otp_to_check}})// Redirect to dashboard
    } else {
      console.log("Ab aayega")
      toast.error(response.data.message);
  } 
}
  catch (error) {
    toast.error('Otp not there')
    console.error("Cannot Login", error);
    throw error;
  }
  
}
  async function submitHandler(event)
  {

    event.preventDefault();
  console.log("Ha")
  
  await postdata();

  }
  
 

  return (
    <div>
      <br />
      <br />
      { <form onSubmit={submitHandler}>
      <label className="Ut">
          <p>Username</p>
          
          <input required 
          type="text"
          value={form.username}
          onChange={changeHandler}
          name="username"
          placeholder="Enter your username"
          />
        </label>
        <label className="Ut">
          <p>Email Address</p>
         
          <input required 
          type="email"
          value={form.email}
          onChange={changeHandler}
          name="email"
          placeholder="Enter your email id here"
          />
        </label>

       
      <br />
      <br />

       <button>Send OTP</button>
      </form>}

     
    </div>
  );
}
export default Forgot;