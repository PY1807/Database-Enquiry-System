import React from "react";

const Home = ({setHome,setRegister,setChat,setLogin}) => {
  setLogin(true);
  setHome(false);
  setRegister(true);
  setChat(true);
  return (
    <div>
      <h1>Home</h1>
    </div>
  );
}
export default Home;