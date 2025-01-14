import React, { useState } from 'react'
import styles from './chatMessages.module.css'

type props = {
    sender: String
    content: String
    timestamp: number | string | Date
    isOutgoing: Boolean
}

const ChatMessages = (props:props) => {
  const messageClass = props.isOutgoing ? styles['outgoing'] : styles['incoming'];
  const [expanded, setExpanded] = useState(false);

  const clickButtonHandler = () => {
    setExpanded((prev) => !prev);
  }
  
  return (
    <div className={`${styles['message']} ${messageClass}`}>
        {/* Absender */}
        <div className={styles['sender']}>
            {props.sender}
        </div>

        {/* Inhalt */}
        <div className={styles['content']}>
            {props.content}
            {!props.isOutgoing && (
                <button className={styles['explain_button']} onClick={clickButtonHandler}>
                    <img className={styles['icon']} src={'/question_white.png'}/>
                </button>
            )}
        </div>

        {/* Zeit */}
        <div className={styles['timestamp']}>{new Date(props.timestamp).toLocaleTimeString()}</div>

        {/* Aufgeklappte Nachricht mit Explainability Infos */}
        {expanded && (
            <div className={styles['expandedContent']}>
              Hello World
            </div>
        )}
    </div>
  )
}

export default ChatMessages