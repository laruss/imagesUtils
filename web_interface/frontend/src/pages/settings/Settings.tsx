import {api} from "../../app/api";
import useErrorHandler from "../../helpers/useErrorHandler";
import {useEffect} from "react";
import {selectSettingsFields} from "../../app/slices/settingsSlice";
import {useAppSelector} from "../../app/hooks";
import {isObjectEmpty} from "../../helpers/methods";
import Form from "./Form";

const Settings = () => {
    const settingsFields = useAppSelector(selectSettingsFields);

    const [getSettings, { error: errorSettings }] = api.useLazyGetSettingsQuery();

    useErrorHandler({
        error: errorSettings,
        message: 'Error while fetching settings data'
    });

    useEffect(() => {
        getSettings({});
    }, [getSettings]);


    if (isObjectEmpty(settingsFields))
        return <div><h1>Loading...</h1></div>;

    return (
        <Form fields={settingsFields}/>
    );
};

export default Settings;