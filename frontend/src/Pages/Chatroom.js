import React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import './Chatroom.css';
import axios from 'axios';
import { useEffect } from 'react';

const Chatroom = ({username}) => {
  console.log("Chatroom")
  
  // console.log(id)
  const navigate=useNavigate();
  const [chat, setChat] = useState([{sender:`Ash`,message:`Hi ${username}, how can I help you?`}]);
  const [newChat, setnewChat] = useState('');
  
  
  
  function clickHandler()
  {
    navigate(-1);
  }

  // useEffect(() => {
  //   // Fetch messages from the backend for the specific room
  //   fetchMessages();
  // }, []);
  const endpoint1=`/messages/`
  const fetchMessages = async () => {
    // Fetch messages from the backend and set them to state
    const response = await axios.get(endpoint1);
    const data = response.data.chat;
    console.log(data);
    setChat(data);
  };
   
   const endpoint='/newmessage/';
  async function handleSendMessage (){
    // Send new message to the backend
    const data={username,newChat};
    setChat((prev)=>[...prev,{sender:username,message:newChat}])
    const response = await axios.post(endpoint, data);
    setnewChat('');
    // fetchMessages();
     // Refresh messages
     setChat((prev)=>[...prev,{sender:`Ash`,message:response.data.result}])
  };
  return (
    <div className="Chatroom">
      <div className='left'>
        <br/>
        <br />
        <br />
        <button className='button-8' onClick={clickHandler}>Back to Chatroom Page</button>
      </div>
      <div className='right'>
      <div className="messages">
       
      
  {chat.map((msg, index) => (
    <div key={index} className="message">
      {msg.sender === username ? (
        <div className="Mine">{msg.message}</div> // Show only message if sender is current user
      ) : (
        <div className="sender">
          {Array.isArray(msg.message) ? (
            msg.message.map((item, idx) => (
              <div key={idx}>
                {Object.keys(item).map((key, kIdx) => (
                  <div key={kIdx}>
                    <strong>{key}:</strong> {item[key]}
                  </div>
                ))}
              </div>
            ))
          ) : (
            <div>{msg.message}</div>
          )}
        </div>

      )}
    </div>
  ))}
</div>


        <div className="new-message">
          <input
            type="text"
            value={newChat}
            onChange={(e) => setnewChat(e.target.value)}
            placeholder="Type your message here"
          />
          {/* <br></br>
          <br></br>
          <br></br> */}
          <button className="button-17" onClick={handleSendMessage}>Send</button>
        </div>
      </div>

    </div>
  );
}

export default Chatroom;

