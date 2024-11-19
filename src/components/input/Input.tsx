import React from 'react'
import styles from './input.module.css'

type props = {
  onChangeRequestHandler: (event:any) => void
}

const Input = (props:props) => {
  return (
    <div>
        <form>
            <input className={styles['input']} onChange={event => {props.onChangeRequestHandler(event)}}/>
        </form>
    </div>
  )
}

export default Input