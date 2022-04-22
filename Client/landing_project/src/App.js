import './App.css';
import Header from './components/Header'
import SideMenuBar from "./components/SideMenuBar";


import Login from './pages/Login/Login'
import {useEffect, useState} from 'react';


function App() {
    const [login, setLogin] = useState(true);

  return (
    <>
        {login ? (
            <>
                <Header />
                <div className="container">
                    <SideMenuBar />
                </div>
            </>
        ) : (
            <Login />
        )}


    </>
  );
}

export default App;
