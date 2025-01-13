// import React from 'react'
// import styles from './input.module.css'

// type props = {

// }

// const Input = (props:props) => {
//   return (
//     <div>
//         <form>
//             <input className={styles['input']}/>
//         </form>
//     </div>
//   )
// }

// export default Input

import React from 'react'
import styles from './input.module.css'

type props = {
  newMessageText: string;
  setNewMessageText: (event:any) => void;
  onSend: () => void;
}

const Input = (props:props) => {
  const handleSubmit = (event:any) => {
    event.preventDefault();
    props.onSend();
  };

  return (
    <div>
        <form className={styles['form']} onSubmit={(event) => handleSubmit(event)}>
            <input className={styles['input']} value={props.newMessageText} onChange={event => {props.setNewMessageText(event.target.value)}} placeholder='Chatte mit MedChat...'/>
            <button type="submit" className={styles['button']}>
                <img className={styles['icon']} src={'/arrow.png'}/>
            </button>
        </form>
    </div>
  )
}

export default Input