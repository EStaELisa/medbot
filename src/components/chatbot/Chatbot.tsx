"use client";

import { useState } from 'react';
import styles from './Chatbot.module.css'
import Header from '../header/Header';
import Body from '../body/Body';
import Input from '../input/Input';
import InputButton from '../inputButton/InputButton';
import { timeStamp } from 'console';


const Chatbot = () => {
    const [messages, setMessages] = useState([
        {sender: 'MedChat', content: 'Hello! What may I do for you?', timeStamp: Date.now(), isOutgoing: false},
    ]);
    const [newMessageText, setNewMessageText] = useState("");

    const onChangeRequestHandler = (event:any) => {
        setNewMessageText(event.target.value);
    }

    const onClickHandler = () => {
        if (newMessageText.trim() === ""){
            return;
        }

        const newMessage = {
            sender: "Me",
            content: newMessageText,
            timeStamp: Date.now(),
            isOutgoing: true
        };

        setMessages((prevMessages) => [... prevMessages, newMessage])
        setNewMessageText("");
        //TODO: add response
    }

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
                        <Input onChangeRequestHandler={onChangeRequestHandler}/>
                    </div>
                    <div className={styles['button']}>
                        <InputButton onClickHandler={onClickHandler}/>
                    </div>
                </div>
        </div>
    )
}

export default Chatbot