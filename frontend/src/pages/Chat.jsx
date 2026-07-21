import PdfUpload from "../components/PdfUpload";
import PdfList from "../components/PdfList";
import Sidebar from "../components/Sidebar";
import api from "../services/api";
import { useState, useEffect, useRef } from "react";
import ChatBubble from "../components/ChatBubble";
import TypingLoader from "../components/TypingLoader";
import {
    Box,
    TextField,
    Button,
    CircularProgress
} from "@mui/material";
function Chat() {
    const user = JSON.parse(localStorage.getItem("user"));
    console.log("USER =", user);
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const bottomRef = useRef(null);
    const [refresh, setRefresh] = useState(false);
    const [conversationId, setConversationId] = useState(null);
    useEffect(() => {
    bottomRef.current?.scrollIntoView({
        behavior: "smooth"
    });
}, [messages]);
    const sendMessage = async () => {
        setLoading(true);
        console.log({
    user_id: user.id,
    question
});
        try {
        const response = await api.post("/chat", {
    user_id: user.id,
    question: question,
    conversation_id: conversationId
});
setConversationId(response.data.conversation_id);
            setMessages((prev) => [
    ...prev,
    {
        question,
        answer: response.data.answer,
        sources: response.data.sources || []
    }
]);
            setQuestion("");
        } catch (error) {
            console.error("Chat Error", error);
        }
        setLoading(false);
    };

    const loadChat = (chat) => {
    setMessages([
        {
            question: chat.question,
            answer: chat.answer,
            sources: chat.sources || []
        }
    ]);
};
    const loadHistory = async () => {
    try {
        const response = await api.get(
            `/chat-history/${user.id}`
        );

        setHistory(response.data.history);
    } catch (error) {
        console.log(error);
    }
};  
useEffect(() => {
    loadHistory();
}, []);
    const newChat = async () => {
    try {
        const res = await api.post(`/new-conversation/${user.id}`);
        setConversationId(res.data.conversation_id);
        setMessages([]);
        setQuestion("");
        setCurrentConversationId(null);
        loadHistory();
    } catch (err) {
        console.log(err);
    }
};

    return(
        <><Sidebar
            history={history}
            loadChat={loadChat}
            newChat={newChat} /><Box
                sx={{
                    flex: 1,
                    display: "flex",
                    flexDirection: "column",
                    ml: "260px"
                }}
            >

                <Box
                    sx={{
                        flex: 1,
                        overflowY: "auto",
                        p: 3
                    }}
                >
                    {messages.map((msg, index) => (
                        <Box key={index}>
                            <ChatBubble sender="user" text={msg.question} />
                            <ChatBubble sender="ai" text={msg.answer} />
                        </Box>
                    ))}

                    {loading && <TypingLoader />}
                    <div ref={bottomRef}></div>
                </Box>

                <Box
                    sx={{
                        display: "flex",
                        p: 2,
                        bgcolor: "#40414f"
                    }}
                >
                    <TextField
                        fullWidth
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder="Ask anything..."
                        sx={{ bgcolor: "black", borderRadius: 1 }} />

                    <Button
                        variant="contained"
                        sx={{ ml: 2 }}
                        onClick={sendMessage}
                    >
                        Send
                    </Button>
                </Box>

            </Box>
        </>
    );
}

export default Chat;