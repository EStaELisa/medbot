"use client";

import { useState } from 'react';
import styles from './Chatbot.module.css'
import Header from '../header/Header';
import Body from '../body/Body';
import Input from '../input/Input';
import InputButton from '../inputButton/InputButton';


const Chatbot = () => {
    // const [messages, setMessages] = useState([]);
    // const [newMessage, setNewMessage] = useState('');

    // const submitNewMessage = async () => {
    //     // Logik zum Senden der Nachricht an die API
    // };

    return (
        <div className={styles['chatbot']}>
            <div className={styles['header']}>
                <Header/>
            </div>
            <div className={styles['chatContainer']}>
                <Body/>
            </div>
                <div className={styles['inputContainer']}>
                    <div className={styles['input']}>
                        <Input/>
                    </div>
                    <div className={styles['button']}>
                        <InputButton/>
                    </div>
                </div>
        </div>
    )
}

export default Chatbot