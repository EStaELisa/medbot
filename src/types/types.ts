export type Message = {
    sender: string;
    content: string;
    timeStamp: Date;
    isOutgoing: boolean;
    htmlFile?: string;
}