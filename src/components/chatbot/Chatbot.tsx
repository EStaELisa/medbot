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
        { sender: 'Me', content: 'I just want to chat!', timeStamp: Date.now(), isOutgoing: true},
        { sender: 'MedChat', content: ' Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', timeStamp: Date.now(), isOutgoing: false},
        { sender: 'Me', content: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua', timeStamp: Date.now(), isOutgoing: true},
        { sender: 'MedChat', content: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren!', timeStamp: Date.now(), isOutgoing: false}
    ]);
    const [newMessageText, setNewMessageText] = useState("");

    // const onChangeRequestHandler = (event:any) => {
    //     setNewMessageText(event.target.value);
    // }

    const onSendMessageHandler = () => {
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
                        <Input newMessageText={newMessageText} setNewMessageText={setNewMessageText} onSend={onSendMessageHandler}/>
                    </div>
                    {/* <div className={styles['button']}>
                        <InputButton onClickHandler={onClickHandler}/>
                    </div> */}
                </div>
        </div>
    )
}

export default Chatbot