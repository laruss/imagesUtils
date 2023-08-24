import {api} from "../../../app/api";
import useErrorHandler from "../../../helpers/useErrorHandler";
import {useEffect} from "react";
import {showLoader, showNotification} from "../../../helpers/dispatchers";

const useNewImageMutation = () => {
    const [
        mutationTrigger,
        { error, data, isLoading }
    ] = api.useNewImageMutation();

    useErrorHandler({ error, message: data?.message || `Error while creating an image` });

    useEffect(() => {
        if (data) {
            data && showNotification(data?.message || `Image was created`, 'success');
        }
    }, [data]);

    useEffect(() => showLoader(isLoading), [isLoading]);

    return {mutationTrigger};
};

export default useNewImageMutation;