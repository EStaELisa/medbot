import React, {useRef} from 'react'
import styles from './input.module.css'

type props = {
    newMessageText: string;
    setNewMessageText: (event: any) => void;
    onSend: () => void;
}

const Input = (props: props) => {
    const textAreaRef = useRef<HTMLTextAreaElement>(null);

    const handleSubmit = (event: any) => {
        event.preventDefault();
        props.onSend();
    };

    const handleKeyDown = (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent the default "Enter" key action (new line in textarea)
            handleSubmit(event); // Trigger form submission
        }
    };

    const autoResize = () => {
        if (textAreaRef.current) {
            textAreaRef.current.style.height = 'auto';
            textAreaRef.current.style.height = textAreaRef.current.scrollHeight + 'px';
        }
    }

    const handleChange = (event: any) => {
        props.setNewMessageText(event.target.value);
        autoResize();
    }

    return (
        <div>
            <form className={styles['form']} onSubmit={(event) => handleSubmit(event)}>
              <textarea
                  ref={textAreaRef}
                  className={styles['input']}
                  value={props.newMessageText}
                  onChange={handleChange}
                  onKeyDown={handleKeyDown}
                  placeholder='Chatte mit MedChat...'
                  rows={1}
                  style={{overflow: 'hidden'}}
              />
                <button type="submit" className={styles['button']}>
                    <img className={styles['icon']} src={'/double-arrow.png'}/>
                </button>
            </form>
        </div>
    )
}

export default Input