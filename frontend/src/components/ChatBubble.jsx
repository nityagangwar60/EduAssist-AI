import {
    Box,
    Paper,
    Typography,
    IconButton
} from "@mui/material";

import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import ReactMarkdown from "react-markdown";
function ChatBubble({ sender, text }) {

    const user = sender === "user";

    return (

        <Box
            sx={{
                display: "flex",
                justifyContent: user ? "flex-end" : "flex-start",
                mb: 2
            }}
        >

            <Paper
                sx={{
                    p: 2,
                    maxWidth: "75%",
                    bgcolor: user ? "#10a37f" : "#343541",
                    color: "white"
                }}
            >

                <Typography
                    variant="subtitle2"
                    sx={{ mb: 1 }}
                >

                    {user ? "You" : "EduAssist AI"}

                </Typography>

                <ReactMarkdown>
                    
                    {text}

                </ReactMarkdown>
                <Box
    sx={{
        display: "flex",
        justifyContent: "flex-end",
        mt: 1
    }}
>

    <IconButton
        size="small"
        onClick={() => navigator.clipboard.writeText(text)}
    >

        <ContentCopyIcon
            fontSize="small"
            sx={{ color: "white" }}
        />

    </IconButton>

                </Box>
            </Paper>
        </Box>
    );

}

export default ChatBubble;