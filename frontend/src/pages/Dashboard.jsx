import { useEffect, useState } from "react";
import api from "../services/api";
import { Box, Paper, Typography } from "@mui/material";

function Dashboard() {

    const user = JSON.parse(localStorage.getItem("user"));

    const [data, setData] = useState({});

    useEffect(() => {

        api.get(`/dashboard/${user.id}`)
            .then(res => setData(res.data));

    }, []);

    return (

        <Box
            sx={{
                display: "grid",
                gridTemplateColumns: "repeat(4,1fr)",
                gap: 3,
                p: 4
            }}
        >

            <Paper sx={{ p: 3 }}>
                <Typography variant="h6">Chats</Typography>
                <Typography variant="h3">
                    {data.total_chats}
                </Typography>
            </Paper>

            <Paper sx={{ p: 3 }}>
                <Typography variant="h6">Conversations</Typography>
                <Typography variant="h3">
                    {data.total_conversations}
                </Typography>
            </Paper>

            <Paper sx={{ p: 3 }}>
                <Typography variant="h6">PDFs</Typography>
                <Typography variant="h3">
                    {data.total_pdfs}
                </Typography>
            </Paper>

            <Paper sx={{ p: 3 }}>
                <Typography variant="h6">
                    Knowledge Base
                </Typography>

                <Typography variant="h5">

                    {data.knowledge_base ? "Ready ✅" : "Empty ❌"}

                </Typography>

            </Paper>

        </Box>

    );

}

export default Dashboard;