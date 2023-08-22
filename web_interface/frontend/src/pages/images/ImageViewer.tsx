import React from "react";
import ImageGallery from "react-image-gallery";
import {Box} from "@mui/material";
import {useAppSelector} from "../../app/hooks";
import {selectChangedImageData} from "../../app/slices/imagesSlice";

interface ImageViewerProps {
    image: string;
}

const ImageViewer = ({image}: ImageViewerProps) => {
    const link = `/api/images/${image}`;
    const currentImageData = useAppSelector(selectChangedImageData);

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