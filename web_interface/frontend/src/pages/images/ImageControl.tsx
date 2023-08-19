import {Box} from "@mui/material";
import ImageViewer from "./ImageViewer";
import {useAppSelector} from "../../app/hooks";
import {selectCurrentImage} from "../../app/slices/imagesSlice";
import OneImageActions from "./OneImageActions";
import ImageForm from "./ImageForm";

const ImageControl = () => {
    const currentImage = useAppSelector(selectCurrentImage);

    if (!currentImage) return null;

    return (
        <Box style={{display: 'flex'}}>
            <Box style={{flex: 2}}>
                <ImageViewer image={currentImage}/>
                <OneImageActions image={currentImage}/>
            </Box>
            <Box style={{flex: 1}}>
                <ImageForm imageId={currentImage}/>
            </Box>
        </Box>
    );
};

export default ImageControl;