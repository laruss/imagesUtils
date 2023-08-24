import {Box} from "@mui/material";
import ImageViewer from "./ImageViewer";
import {useAppSelector} from "../../app/hooks";
import {selectCurrentImage, selectNewImage} from "../../app/slices/imagesSlice";
import OneImageActions from "./OneImageActions";
import ImageForm from "./ImageForm";

const ImageControl = () => {
    const currentImage = useAppSelector(selectCurrentImage);
    const newImage = useAppSelector(selectNewImage);

    if (!currentImage) return null;

    return (
        <Box style={{display: 'flex'}}>
            <Box style={{flex: 2}}>
                <ImageViewer image={currentImage} newImage={newImage}/>
                <OneImageActions image={currentImage} newImage={newImage}/>
            </Box>
            <Box style={{flex: 1}}>
                <ImageForm imageId={currentImage} newImage={newImage}/>
            </Box>
        </Box>
    );
};

export default ImageControl;