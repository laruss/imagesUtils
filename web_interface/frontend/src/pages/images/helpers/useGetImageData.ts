import {api} from "../../../app/api";
import useErrorHandler from "../../../helpers/useErrorHandler";
import {useEffect} from "react";

const useGetImageData = (imageId: string) => {
    const [getImageData, {error}] = api.useLazyGetImageDataQuery();

    useErrorHandler({error, message: "Error while fetching image data"});

    useEffect(() => { getImageData(imageId) }, [getImageData, imageId]);
};

export default useGetImageData;