import React from 'react'
import styles from './body.module.css'
import ChatMessages from '../chatMessages/ChatMessages'
import Input from '../input/Input'

const Body = () => {
  const messages = [
    { sender: 'Me', content: 'Hello', timeStamp: Date.now(), isOutgoing: true},
    { sender: 'MedChat', content: 'Hello! How can I help you?', timeStamp: Date.now(), isOutgoing: false},
    { sender: 'Me', content: 'I just want to chat!', timeStamp: Date.now(), isOutgoing: true},
  ]

  return (
    <div className={styles['chatContainer']}>
      <div className={styles['messageContainer']}>
        {messages.map((msg, idx) => (
          <ChatMessages key={idx} sender={msg.sender} content={msg.content} timestamp={msg.timeStamp} isOutgoing={msg.isOutgoing}/>
        ))}
      </div>
    </div>
  )
}

export default Body