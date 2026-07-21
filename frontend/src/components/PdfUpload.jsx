import { useState } from "react";
import api from "../services/api";

import {
    Button,
    Box,
    Typography,
    Snackbar,
    Alert,
    CircularProgress
} from "@mui/material";

import UploadFileIcon from "@mui/icons-material/UploadFile";

function PdfUpload({ onUpload }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const [open, setOpen] = useState(false);
    const [message, setMessage] = useState("");
    const [severity, setSeverity] = useState("success");

    const uploadPdf = async () => {

        if (!file) {

            setSeverity("warning");
            setMessage("Please select a PDF");
            setOpen(true);
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        setLoading(true);

        try {

            const res = await api.post(
                "/upload-pdf",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            );

            setSeverity("success");
            setMessage(res.data.message);
            if (onUpload) {
    onUpload();
}
            setFile(null);

        } catch (err) {

            console.log(err);

            setSeverity("error");
            setMessage("Upload Failed");

        }

        setLoading(false);
        setOpen(true);

    };

    return (

        <Box sx={{ p: 2 }}>

            <Button
                component="label"
                variant="outlined"
                startIcon={<UploadFileIcon />}
                fullWidth
            >
                Choose PDF

                <input
                    hidden
                    type="file"
                    accept=".pdf"
                    onChange={(e) =>
                        setFile(e.target.files[0])
                    }
                />

            </Button>

            {
                file &&
                <Typography
                    variant="body2"
                    sx={{
                        mt: 1,
                        color: "white"
                    }}
                >
                    {file.name}
                </Typography>
            }

            <Button
                variant="contained"
                fullWidth
                sx={{ mt: 2 }}
                onClick={uploadPdf}
                disabled={loading}
            >
                {
                    loading
                        ? <CircularProgress size={20} color="inherit" />
                        : "Upload PDF"
                }
            </Button>

            <Snackbar
                open={open}
                autoHideDuration={3000}
                onClose={() => setOpen(false)}
            >

                <Alert
                    severity={severity}
                    variant="filled"
                >
                    {message}
                </Alert>

            </Snackbar>

        </Box>

    );

}

export default PdfUpload;