"use client";

import { useState } from 'react';
import Header from '../header/Header';


const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');

    const submitNewMessage = async () => {
        // Logik zum Senden der Nachricht an die API
    };

    return (
        <div>
            <Header/>
        </div>
    )
}

export default Chatbot