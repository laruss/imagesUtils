import {api} from "../../../app/api";
import useErrorHandler from "../../../helpers/useErrorHandler";
import {useEffect} from "react";

interface Props {
    imageId: string;
    newImage: string | null;
}

const useGetImageData = ({imageId, newImage}: Props) => {
    const [getImageData, {error}] = api.useLazyGetImageDataQuery();

    useErrorHandler({error, message: "Error while fetching image data"});

    useEffect(() => {
        (imageId && !newImage) && getImageData(imageId);
    }, [getImageData, imageId, newImage]);
};

export default useGetImageData;