import Image from "next/image";
import styles from "./page.module.css";
import Chatbot from "@/components/chatbot/Chatbot";

export default function Home() {
  return (
    <div>
      <Chatbot/>
    </div>
  );
}
