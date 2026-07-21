import PdfUpload from "./PdfUpload";
import PdfList from "./PdfList";

import {
    Drawer,
    Toolbar,
    Typography,
    List,
    ListItemButton,
    ListItemText,
    Divider,
    Button
} from "@mui/material";

function Sidebar({
    history,
    loadChat,
    newChat
}) {

    return (

        <Drawer
            variant="permanent"
            sx={{
                width:260,
                "& .MuiDrawer-paper":{
                    width:260,
                    background:"#202123",
                    color:"white"
                }
            }}
        >

            <Toolbar>

                <Typography variant="h6">
                    EduAssist AI
                </Typography>

            </Toolbar>

            <Button
    variant="contained"
    sx={{ m: 2 }}
    onClick={newChat}
>
    + New Chat
</Button>

<Divider />

<div style={{ padding: "10px" }}>
    <PdfUpload />
</div>

<div style={{ padding: "10px" }}>
    <PdfList />
</div>

<Divider />
            <List>

                {
                    history.map((chat)=>(
                        <ListItemButton
                            key={chat.id}
                            onClick={()=>loadChat(chat)}
                        >

                            <ListItemText
                                primary={chat.question}
                            />

                        </ListItemButton>
                    ))
                }

            </List>

        </Drawer>

    );

}

export default Sidebar;