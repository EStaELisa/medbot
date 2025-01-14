import React, { useState } from 'react'
import styles from './chatMessages.module.css'
import { Html } from 'next/document';

type props = {
    sender: String;
    content: String;
    timestamp: number | string | Date;
    isOutgoing: Boolean;
    htmlFile?: string;
}

const ChatMessages = (props:props) => {
  const messageClass = props.isOutgoing ? styles['outgoing'] : styles['incoming'];

  const clickButtonHandler = () => {
    if (!props.htmlFile){
      return;
    }
    window.open(props.htmlFile, '_blank');
  }
  
  return (
    <div className={`${styles['message']} ${messageClass}`}>
        {/* Absender */}
        <div className={styles['sender']}>
            {props.sender}
        </div>

        {props.htmlFile}
        {/* Inhalt */}
        <div className={styles['content']}>
            {props.content}
            {!props.isOutgoing && props.htmlFile &&(
                <button className={styles['explain_button']} onClick={clickButtonHandler}>
                    <img className={styles['icon']} src={'/question_white.png'}/>
                </button>
            )}
        </div>

        {/* Zeit */}
        <div className={styles['timestamp']}>{new Date(props.timestamp).toLocaleTimeString()}</div>
    </div>
  )
}

export default ChatMessages