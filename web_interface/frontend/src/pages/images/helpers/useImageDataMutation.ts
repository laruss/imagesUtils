import {UseMutation} from "@reduxjs/toolkit/dist/query/react/buildHooks";
import {MutationDefinition} from "@reduxjs/toolkit/query";
import useErrorHandler from "../../../helpers/useErrorHandler";
import {useEffect} from "react";
import {showLoader, showNotification} from "../../../helpers/dispatchers";

interface ImageDataInterface {
    actionName: string;
    apiMutationMethod: UseMutation<MutationDefinition<any, any, any, any, any>>;
    callback?: () => void;
}

const useImageDataMutation = ({apiMutationMethod, actionName, callback}: ImageDataInterface) => {
    const [
        mutationTrigger,
        { error, data, isLoading }
    ] = apiMutationMethod();

    useErrorHandler({ error, message: `Error while ${actionName}` });

    useEffect(() => {
        if (data) {
            showNotification(`${actionName} is done`, 'success');
            callback && callback();
        }
    }, [data]);

    useEffect(() => showLoader(isLoading), [isLoading]);

    return {mutationTrigger};
};

export default useImageDataMutation;