import React, { useEffect, useRef } from 'react'
import styles from './body.module.css'
import ChatMessages from '../chatMessages/ChatMessages'
import { Message } from '@/types/types'

type props = {
  messages: [Message];
}

const Body = (props:props) => {
  // Fürs Scrollen zur aktuellsten Nachricht, weil man sonst immer selbst komplett runter scrollen müsste
  const messagesEndRef = useRef<HTMLDivElement>(null);
  useEffect(() => {messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });}, [props.messages])


  return (
    <div className={styles['chatContainer']}>
      <div className={styles['messageContainer']}>
        {/* Auflisten aller Nachrichten */}
        {props.messages.map((msg, idx) => (
          <ChatMessages key={idx} sender={msg.sender} content={msg.content} timestamp={msg.timeStamp} isOutgoing={msg.isOutgoing} htmlFile={msg.htmlFile}/>
        ))}
      </div>
      <div ref={messagesEndRef}/>
    </div>
  )
}

export default Body