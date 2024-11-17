"use client";

import { useState } from 'react';


const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');

    const submitNewMessage = async () => {
        // Logik zum Senden der Nachricht an die API
    };

    return (
        <div>Chatbot</div>
    )
}

export default Chatbot