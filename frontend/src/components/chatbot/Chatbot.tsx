"use client";

import { useState } from 'react';
import styles from './Chatbot.module.css'
import Header from '../header/Header';
import Body from '../body/Body';
import Input from '../input/Input';


const Chatbot = () => {
    // Zum Testen ohne tatsächliche Einträge (mit Verlinkung zur Explainability-HTML)
    // const testarray = [
    //     {sender: 'MedChat', content: 'Hello! What may I do for you?', timeStamp: Date.now(), isOutgoing: false},
    //     { sender: 'Me', content: 'I just want to chat!', timeStamp: Date.now(), isOutgoing: true},
    //     { sender: 'MedChat', content: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', timeStamp: Date.now(), isOutgoing: false, htmlFile: '/file.html'},
    //     { sender: 'Me', content: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua', timeStamp: Date.now(), isOutgoing: true},
    //     { sender: 'MedChat', content: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren!', timeStamp: Date.now(), isOutgoing: false}
    // ]
    // const [messages, setMessages] = useState(testarray);


    const [messages, setMessages] = useState([{ sender: 'MedChat', content: 'Hallo, wie kann ich helfen?', timeStamp: Date.now(), isOutgoing: false }]);
    const [newMessageText, setNewMessageText] = useState("");

    const onSendMessageHandler = async () => {
    if (newMessageText.trim() === "") {
        return;
    }

    const newMessage = {
      sender: "Me",
      content: newMessageText,
      timeStamp: Date.now(),
      isOutgoing: true
    };

    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setNewMessageText("");
    try {
        // Send the message to the server
        const response = await fetch("http://localhost:80/message/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: newMessageText }) // Request body with the correct format
        });

        if (!response.ok) {
            console.error("Failed to send the message", response.statusText);
            return;
        }
        const responseData = await response.json();
        console.log("Response from server:", responseData);
        // Construct the new message object locally for the UI
        const answerMessage  = {
            sender: "MedChat",
            content: responseData.message_received,
            timeStamp: Date.now(),
            isOutgoing: false
        };


        // Update the local messages state
        setMessages((prevMessages) => [...prevMessages, answerMessage]);
    } catch (error) {
        console.error("Error sending the message:", error);
    }
    };

    return (
        <div className={styles['chatbot']}>
            <div className={styles['header']}>
                <Header/>
            </div>
            <div className={styles['chatContainer']}>
                <Body messages={messages}/>
            </div>
                <div className={styles['inputContainer']}>
                    <div className={styles['input']}>
                        <Input newMessageText={newMessageText} setNewMessageText={setNewMessageText} onSend={onSendMessageHandler}/>
                    </div>
                </div>
        </div>
    )
}

export default Chatbot