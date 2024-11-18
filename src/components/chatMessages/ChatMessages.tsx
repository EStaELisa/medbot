import React from 'react'
import styles from './chatMessages.module.css'

type props = {
    sender: String
    content: String
    timestamp: number | string | Date
    isOutgoing: Boolean
}

const ChatMessages = (props:props) => {
  const messageClass = props.isOutgoing ? styles['outgoing'] : styles['incoming'];
  
  return (
    <div className={`${styles['message']} ${messageClass}`}>
        <div className={styles['sender']}>{props.sender}</div>
        <div className={styles['content']}>{props.content}</div>
        <div className={styles['timestamp']}>{new Date(props.timestamp).toLocaleTimeString()}</div>
    </div>
  )
}

export default ChatMessages