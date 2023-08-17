import {Box} from "@mui/material";
import ImageViewer from "./ImageViewer";
import ImageData from "./ImageData";
import {useAppSelector} from "../../app/hooks";
import {selectCurrentImage} from "../../app/slices/imagesSlice";
import ImageActions from "./ImageActions";

const ImageForm = () => {
    const currentImage = useAppSelector(selectCurrentImage);

    if (!currentImage) return null;

    return (
        <Box style={{display: 'flex'}}>
            <Box style={{flex: 2}}>
                <ImageViewer image={currentImage}/>
                <ImageActions image={currentImage}/>
            </Box>
            <Box style={{flex: 1}}>
                <ImageData image={currentImage}/>
            </Box>
        </Box>
    );
};

export default ImageForm;