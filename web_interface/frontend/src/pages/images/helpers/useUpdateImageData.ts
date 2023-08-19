import {api} from "../../../app/api";
import useErrorHandler from "../../../helpers/useErrorHandler";
import {useEffect} from "react";
import {showLoader, showNotification} from "../../../helpers/dispatchers";

const useUpdateImageData = () => {
    const [
        updateImageData,
        {error, data, isLoading}
    ] = api.useUpdateImageDataMutation();

    useErrorHandler({error, message: "Error while updating image data"});

    useEffect(() => showLoader(isLoading), [isLoading]);
    useEffect(() => {data && showNotification(`Image data updated`, 'success');}, [data]);

    return {updateImageData};
};

export default useUpdateImageData;