import React from "react";
import ImageGallery from "react-image-gallery";
import {Box} from "@mui/material";
import UploadFromSourceForm from "./UploadFromSourceForm";

interface ImageViewerProps {
    image: string;
    newImage: null | string;
}

const ImageViewer = ({image, newImage}: ImageViewerProps) => {
    const link = `/api/images/${image}`;

    return (
        <Box style={{height: '85vh', overflow: 'auto'}}>
            {
                newImage ? (
                    <UploadFromSourceForm imageId={newImage}/>
                ) : (
                    <ImageGallery
                        items={[{ original: link }]}
                        renderFullscreenButton={()=>null}
                        renderPlayPauseButton={()=>null}
                    />
                )
            }
        </Box>
    );
};

export default ImageViewer;