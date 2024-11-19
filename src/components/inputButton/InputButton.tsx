import React from 'react'
import styles from './inputButton.module.css'

type props = {
  onClickHandler: () => void
}

const InputButton = (props:props) => {
  return (
    <div>
        <button className={styles['button']} onClick={() => props.onClickHandler()}>
            <img className={styles['icon']} src={'/arrow.png'}/>
        </button>
    </div>
  )
}

export default InputButton