import {api} from "../../../app/api";
import useErrorHandler from "../../../helpers/useErrorHandler";
import {useEffect} from "react";
import {showLoader, showNotification} from "../../../helpers/dispatchers";

const useUpdateSettings = () => {
    const [
        updateSettings,
        { error, data, isLoading }
    ] = api.useUpdateSettingsMutation();

    useErrorHandler({ error, message: `Error while updating settings` });

    useEffect(() => {
        if (data && data.message) showNotification(data.message, 'success');
    }, [data]);

    useEffect(() => showLoader(isLoading), [isLoading]);

    return { updateSettings };
};

export default useUpdateSettings;