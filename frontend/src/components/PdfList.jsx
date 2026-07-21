import { useEffect, useState } from "react";
import api from "../services/api";

import {
    Box,
    Typography,
    IconButton,
    Paper,
    Divider
} from "@mui/material";

import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf";
import DeleteIcon from "@mui/icons-material/Delete";

function PdfList() {

    const [pdfs, setPdfs] = useState([]);

    const loadPdfs = async () => {

        try {

            const res = await api.get("/pdfs");

            setPdfs(res.data.files);

        } catch (err) {

            console.log(err);

        }

    };

    useEffect(() => {

        loadPdfs();

    }, []);

    const deletePdf = async (filename) => {

        try {

            await api.delete(`/pdf/${filename}`);

            loadPdfs();

        } catch (err) {

            console.log(err);

        }

    };

    return (

        <Box sx={{ p: 2 }}>

            <Typography
                variant="subtitle1"
                sx={{
                    color: "white",
                    mb: 2,
                    fontWeight: "bold"
                }}
            >
                Uploaded PDFs
            </Typography>

            <Box
                sx={{
                    maxHeight: 250,
                    overflowY: "auto"
                }}
            >

                {

                    pdfs.length === 0 ?

                        <Typography
                            variant="body2"
                            sx={{ color: "gray" }}
                        >
                            No PDFs Uploaded
                        </Typography>

                        :

                        pdfs.map((pdf) => (

                            <Paper
                                key={pdf}
                                sx={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                    p: 1,
                                    mb: 1,
                                    bgcolor: "#2d2d2d",
                                    color: "white"
                                }}
                            >

                                <Box
                                    sx={{
                                        display: "flex",
                                        alignItems: "center",
                                        gap: 1,
                                        overflow: "hidden"
                                    }}
                                >

                                    <PictureAsPdfIcon
                                        color="error"
                                    />

                                    <Typography
                                        variant="body2"
                                        noWrap
                                    >
                                        {pdf}
                                    </Typography>

                                </Box>

                                <IconButton
                                    color="error"
                                    onClick={() => deletePdf(pdf)}
                                >

                                    <DeleteIcon />

                                </IconButton>

                            </Paper>

                        ))

                }

            </Box>

            <Divider sx={{ mt: 2 }} />

        </Box>

    );

}

export default PdfList;