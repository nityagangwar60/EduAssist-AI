import { Box, CircularProgress, Typography } from "@mui/material";

function TypingLoader() {
  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 2,
        p: 2
      }}
    >
      <CircularProgress size={18} />
      <Typography>EduAssist AI is thinking...</Typography>
    </Box>
  );
}

export default TypingLoader;