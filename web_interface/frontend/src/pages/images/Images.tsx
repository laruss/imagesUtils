import {Box} from "@mui/material";
import ImagesList from "./ImagesList";
import ImageForm from "./ImageForm";
import {api} from "../../app/api";
import {useEffect} from "react";
import useErrorHandler from "../../helpers/useErrorHandler";

const Images = () => {
    const [getImages, {error: errorImages}] = api.useLazyGetImagesQuery();

    useErrorHandler({
        error: errorImages,
        message: 'Error while fetching images data'
    });

    useEffect(() => {
        getImages({});
    }, [getImages]);

    return (
        <Box style={{display: 'flex'}}>
            <Box style={{flexGrow: 2}}><ImagesList/></Box>
            <Box style={{flexGrow: 6}}><ImageForm/></Box>
        </Box>
    );
};

export default Images;