import {Box} from "@mui/material";
import ImagesList from "./ImagesList";
import {api} from "../../app/api";
import {useEffect} from "react";
import useErrorHandler from "../../helpers/useErrorHandler";
import ImageControl from "./ImageControl";

const Images = () => {
    const [getImages, {error: errorImages}] = api.useLazyGetImagesQuery();
    const [getImagesDataSchema, {error: errorImagesDataSchema}] = api.useLazyGetImageDataSchemaQuery();

    useErrorHandler({
        error: errorImages,
        message: 'Error while fetching images data'
    });

    useErrorHandler({
        error: errorImagesDataSchema,
        message: 'Error while fetching images data schema'
    });

    useEffect(() => {
        getImagesDataSchema({});
        getImages({});
    }, [getImages, getImagesDataSchema]);

    return (
        <Box style={{display: 'flex'}}>
            <Box style={{flexGrow: 2}}><ImagesList/></Box>
            <Box style={{flexGrow: 6}}><ImageControl/></Box>
        </Box>
    );
};

export default Images;