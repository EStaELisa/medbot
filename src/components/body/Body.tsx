import React from 'react'
import styles from './body.module.css'
import ChatMessages from '../chatMessages/ChatMessages'
import { Message } from '@/types/types'

type props = {
  messages: [Message];
}

const Body = (props:props) => {
  return (
    <div className={styles['chatContainer']}>
      <div className={styles['messageContainer']}>
        {props.messages.map((msg, idx) => (
          <ChatMessages key={idx} sender={msg.sender} content={msg.content} timestamp={msg.timeStamp} isOutgoing={msg.isOutgoing}/>
        ))}
      </div>
    </div>
  )
}

export default Body