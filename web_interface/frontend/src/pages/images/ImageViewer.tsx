import React from "react";
import ImageGallery from "react-image-gallery";
import {Box} from "@mui/material";

interface ImageViewerProps {
    image: string;
}

const ImageViewer = ({image}: ImageViewerProps) => {
    const link = `/api/images/${image}`;

    return (
        <Box style={{height: '85vh', overflow: 'auto'}}>
            <ImageGallery
                items={[{ original: link }]}
                renderFullscreenButton={()=>null}
                renderPlayPauseButton={()=>null}
            />
        </Box>
    );
};

export default ImageViewer;