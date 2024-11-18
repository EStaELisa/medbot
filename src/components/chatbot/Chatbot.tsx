"use client";

import { useState } from 'react';
import styles from './Chatbot.module.css'
import Header from '../header/Header';
import Body from '../body/Body';
import Input from '../input/Input';


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
            <Input/>
        </div>
    )
}

export default Chatbot