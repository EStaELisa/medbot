import React from 'react'
import styles from './inputButton.module.css'

const InputButton = () => {
  return (
    <div>
        <button className={styles['button']}>
            <img className={styles['icon']} src={'/arrow.png'}/>
        </button>
    </div>
  )
}

export default InputButton