import React from 'react'
import styles from './chatMessages.module.css'

type props = {
    sender: String
    content: String
    timestamp: number | string | Date
    isOutgoing: Boolean
}

const ChatMessages = (props:props) => {
  return (
    <div className={styles['']}>
        <div className={styles['sender']}>{props.sender}</div>
        <div className={styles['content']}>{props.content}</div>
        <div className={styles['timestamp']}>{new Date(props.timestamp).toLocaleTimeString()}</div>
    </div>
  )
}

export default ChatMessages