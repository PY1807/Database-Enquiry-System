import React, { useState ,useEffect} from "react";
import { AiOutlineEye,AiOutlineEyeInvisible } from "react-icons/ai";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { useLocation } from "react-router-dom";
const Otp = ({setotpver}) => {

  console.log("YEs Yes Yes");
 
  const location=useLocation();
  const {username,email,otp_to_check}=location.state || {};
  console.log(email)
  const[otp_to,setotp_to]=useState(otp_to_check)
  const [otp,setotp]=useState("");
  const [resend,setresend]=useState(false);
  const [startTime, setStartTime] = useState(Date.now());
  console.log(resend);

    useEffect(() => {
        const checkTime = () => {
            if (Date.now() > (startTime + (5 * 60 * 1000))) {
                setresend(true);
                setStartTime(Date.now());
            }
        };

        const interval = setInterval(checkTime, 1000); // Check every second

        // Cleanup interval on component unmount
        return () => clearInterval(interval);
    }, [startTime]);
  const navigate=useNavigate();
  // const endpoint = `http://127.0.0.1:8000/otpv/`; // Django endpoint http://localhost:8080
  const endpoint = `/otpv/`;
async function postdata() {
  console.log("aa gaye post data ke andar")
  const data = {otp,otp_to};
  try {
    const response = await axios.post(endpoint, data);

    if (response.data.status === "success") {
      toast.success(response.data.message)
      console.log("success")
      setotpver(true);
      navigate("/newpas",{ state: { username}});
      // showpass(true) // Redirect to dashboard
    } else {
      toast.error(response.data.message)
      console.log("Ab aayega")
      
      // toast.error(response.data.message);
  } 
}
  catch (error) {
    console.error("Cannot Login", error);
    throw error;
  }
  // navigate("/forgot")
}
// const endpoint1 = `http://127.0.0.1:8000/otp/`
   const endpoint1 = `/otp/`
async function postdata1() {
  console.log("aa gaye post data ke andar")
  const data = {email};
  try {
    const response = await axios.post(endpoint1, data);

    if (response.data.status === "success") {
      toast.success(response.data.message)
      console.log("success")
      setotp("")
      const new_otp=response.data.otp_to_check;
      setotp_to(new_otp);
      setresend(false);
      // showpass(true) // Redirect to dashboard
    } else {
      toast.error(response.data.message)
      console.log("Ab aayega")
      
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

    event.preventDefault();
  console.log("Ha")
  if(!resend)
  await postdata();
  else
  await postdata1();

  }
  
  function changeHandler1(event)
  {
    console.log("Otp a agaya")
    setotp(event.target.value);
  }
  

  return (
    <div className="U">
      { <form onSubmit={submitHandler}>
      <p>Enter OTP</p>
      <div className="Ut">
      <label className="">
          
          
          <input required 
          type="text"
          value={otp}
          onChange={changeHandler1}
          name="otp"
          />
          
          
        </label>

       

       {resend ? (<button>ReSend Otp</button>) : (<button>Check</button>)}
       
      </div>
       
      
      
      </form>
      }

      

      
      
    </div>
  );
}
export default Otp;