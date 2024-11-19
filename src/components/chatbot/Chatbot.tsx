"use client";

import { useState } from 'react';
import styles from './Chatbot.module.css'
import Header from '../header/Header';
import Body from '../body/Body';
import Input from '../input/Input';
import InputButton from '../inputButton/InputButton';


const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');

    const submitNewMessage = async () => {
        // Logik zum Senden der Nachricht an die API
    };

    return (
        <div className={styles['chatbot']}>
            <Header/>
            <Body/>
            <InputButton/>
        </div>
    )
}

export default Chatbot