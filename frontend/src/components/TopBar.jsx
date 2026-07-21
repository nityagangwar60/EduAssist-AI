import { AppBar, Toolbar, Typography } from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";

function TopBar() {

    return (

        <AppBar position="static">

            <Toolbar>

                <SmartToyIcon sx={{ mr: 2 }} />

                <Typography variant="h6">

                    EduAssist AI

                </Typography>

            </Toolbar>

        </AppBar>

    );

}

export default TopBar;