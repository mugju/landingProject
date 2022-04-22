import React, { useState } from 'react'
import './Login.css'
import {BiUser} from 'react-icons/bi'
import {AiFillLock} from 'react-icons/ai'
import axios from 'axios'
import cookies from 'react-cookies'

export default function Login() {

    const [localId, setLocalId] = useState(localStorage.getItem('userId'));
    const [userId, setId] = useState('aaa@test.com');
    const [remember, setRemember] = useState(false);
    const [userPw, setPw] = useState('123123');
    const [Ok, setOk] = useState(true);
    const getAuth = () => {
        axios.post('http://127.0.0.1:8000/user/signin/',
        {
            user_email: userId,
            user_pw: userPw
        },
            { withCredentials: true }
        ).then((res) =>{
            console.log(res)
            setOk(true);
            remember ? localStorage.setItem('userId',userId) : localStorage.removeItem('userId');
        }).catch((error) => {
            console.log(error);
            setOk(false);
        })
    }
    const testAPI = () => {
        axios.get("http://127.0.0.1:8000/company?page=1")
            .then(res => {
                console.log(res.data)
            })
    }

    return (
        <div>
            <div className='backGround'>
                <p className='titleFont'>Medicla Store</p>
                <p className='undertitleFont'> Management System</p>
                <div className='inputBoard'>
                    <p className='signinTitle'>Sign in</p>
                    <div className='inputBar'>
                        <div>
                            <BiUser className='icon' size='40'></BiUser>
                            <input className='inputele' value={localId !== null ? localId: null} type="text" onChange={e => setId(e.target.value)} ></input>
                        </div>
                        <br />
                        <div>
                            <AiFillLock className='icon' size='40'></AiFillLock>
                            <input className='inputele' type='password' onChange={e => setPw(e.target.value)}></input>
                        </div>
                    </div>
                    <div className='checkBtn'>
                        <input type='checkbox' onClick={setRemember}
                            // checked={localId !== null ? true : false}
                               className='checkbox'></input>
                        <p className='remember'> Remember me </p>
                        <button className='loginBtn' variant="contained" onClick={getAuth}>SIGN IN</button>
                    </div>
                    <div className='forGot'>
                        <p>Forgot Password?</p>
                        <p>Register Now!</p>
                    </div>
                    <div>
                        {
                            Ok ?
                                <div></div>
                                :
                                <div className='failSignin'>
                                    The Account is incorrect
                                </div>
                        }
                    </div>
                    <button onClick={testAPI}>test</button>
                </div>
            </div>
        </div>
    );
}