import FormGroup from "../../components/form/FormGroup";
import {api} from "../../app/api";
import useErrorHandler from "../../helpers/useErrorHandler";
import { useEffect } from "react";
import {selectCurrentImageData} from "../../app/slices/imagesSlice";
import {useAppSelector} from "../../app/hooks";
import {Paper} from "@mui/material";

interface ImageDataProps {
    image: string
}

const ImageData = ({image}: ImageDataProps) => {
    const currentImageData = useAppSelector(selectCurrentImageData);

    const [getImageData, { error: errorImageData }] = api.useLazyGetImageDataQuery();

    useErrorHandler({
        error: errorImageData,
        message: 'Error while fetching image data'
    });

    useEffect(() => {
        getImageData(image);
    }, [getImageData, image]);

    return (
        <Paper style={{height: '85vh', overflow: 'auto'}}>
            <FormGroup name={"Image Data"} fields={currentImageData}/>
        </Paper>
    );
};

export default ImageData;