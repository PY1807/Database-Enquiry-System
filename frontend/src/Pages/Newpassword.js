import React, { useState } from "react";
import { AiOutlineEye,AiOutlineEyeInvisible } from "react-icons/ai";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { useLocation } from "react-router-dom";
import { RxCross1 } from "react-icons/rx";
import { TiTick } from "react-icons/ti";

const Newpassword = () => {

  console.log("YEs Yes Yes");
 
  const location=useLocation();
  const {username}=location.state || {};
  

  const [form,setform]=useState({
    password:"",
    confirmPassword:""
    })
    const[showPassword,setPassword]=useState(false);
    const[showPassword1,setPassword1]=useState(false);
    const [showsymbol,setsymbol]=useState(false);
    const [showsymbol1,setsymbol1]=useState(false);
    const [showsymbol2,setsymbol2]=useState(false);
    const [showsymbol3,setsymbol3]=useState(false);
  
    function changeHandler(event)
    {
      event.preventDefault();
      setform((prev)=>(
        {
          ...prev,
          [event.target.name]:event.target.value
        }
      ))
      if(event.target.name==='password')
        {
          const password=event.target.value;
            let flag1=false,flag2=false,flag3=false,flag=false;
            if(password.length>=8)
              {
                flag=true;
              }
            for(let i=0;i<password.length;i++)
              {
                if(password[i]>='0' && password[i]<='9')
                  {
               
                    flag1=true;
                  }
                  else if(password[i]>='A' && password[i]<='Z')
                    {
                      flag2=true;
                    }
                    else if(password[i]=='@' || password[i]=='$' || password[i]=='#')
                      {
                        flag3=true;
                      }
              }
              setsymbol(flag);
              setsymbol1(flag1);
              
              setsymbol2(flag2);
              setsymbol3(flag3);
        }
     
    }

  const navigate=useNavigate();
  // const endpoint = `http://127.0.0.1:8000/newpass/`; // Django endpoint http://localhost:8080
  const endpoint = `/newpass/`;

async function postdata() {
  console.log("aa gaye post data ke andar")
  const passw=form.password;
  const data = {username,passw};
  try {
    const response = await axios.post(endpoint, data);

    if (response.data.status === "success") {
      toast.success(response.data.message)
      console.log("success")
      navigate("/login")
      // showpass(true) // Redirect to dashboard
    } else {
      toast.error(response.data.message)
      console.log("Ab aayega")
      
    //  fv 
      // toast.error(response.data.message);
  } 
}
  catch (error) {
    console.error("Cannot Login", error);
    throw error;
  }
  // navigate("/forgot")
}

  

  async function submitHandler(event)
  {

    console.log("No");
  event.preventDefault();
  if(showsymbol && showsymbol1 && showsymbol2 && showsymbol3)
    {
      console.log("ha");
      if(form.password!=form.confirmPassword)
        {
          toast.error("Passwords do not match");
          return ;
        }
         await postdata();
      
    }
    else
    {
      toast.error("Conditions for password  not satisfied");
          return ;
    }
  


  }
  
  

  return (
    <div>
    
       <form onSubmit={submitHandler}>
       <div className="U">
  <label className="Ut">
    <p>Create New Password</p>
    <input 
    required
    type= {showPassword?("text"):("password")}
    name="password"
    placeholder="Enter Password here"
    value={form.password}
    onChange={changeHandler}/>
    <span onClick={()=>setPassword((prev)=> !prev)}>
        {showPassword?(<AiOutlineEye/>):(<AiOutlineEyeInvisible/>)}
      </span>
  </label>
  <label className="Ut">
    <p>Confirm Password </p>
    <input 
    required
    type= {showPassword1?("text"):("password")}
    name="confirmPassword"
    placeholder="Confirm Password "
    value={form.confirmPassword}
    onChange={changeHandler}/>
    <span onClick={()=>setPassword1((prev)=> !prev)}>
        {showPassword1?(<AiOutlineEye/>):(<AiOutlineEyeInvisible/>)}
      </span>
  </label>
  </div>
  <br />
  <br />
 
  <div className="Ut1">
    <div className="At">
    <p>
      {
        !showsymbol?(<RxCross1 />):(<TiTick />)
      }
    </p>
    <p>
      {
        !showsymbol1?(<RxCross1 />):(<TiTick />)
      }
    </p>
    <p>
      {
        !showsymbol2?(<RxCross1 />):(<TiTick />)
      }
    </p>
    <p>
      {
        !showsymbol3?(<RxCross1 />):(<TiTick />)
      }
    </p>
    </div>
    <div className="A">
    <span>Password length more than 8</span>
    <span>Presence of a Digit</span>
    <span>Presence of Uppercase Character</span>
    <span>Presence of Special Character</span>
    </div>
  </div>
    
      <button className="but">Update Password</button>
       </form>
        </div>
    );
    }
    
export default Newpassword;