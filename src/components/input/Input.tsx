import React from 'react'
import styles from './input.module.css'

const Input = () => {
  return (
    <div>
        <form>
            <input className={styles['input']}/>
        </form>
    </div>
  )
}

export default Input