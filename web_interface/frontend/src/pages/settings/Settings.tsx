import {api} from "../../app/api";
import useErrorHandler from "../../helpers/useErrorHandler";
import {useEffect} from "react";
import {selectSettingsNewFields, selectSettingsFieldsSchema} from "../../app/slices/settingsSlice";
import {useAppSelector} from "../../app/hooks";
import {isObjectEmpty} from "../../helpers/methods";
import SettingsForm from "./SettingsForm";

const Settings = () => {
    const settingsFields = useAppSelector(selectSettingsNewFields);
    const settingsFieldsSchema = useAppSelector(selectSettingsFieldsSchema);

    const [getSettings, { error: errorSettings }] = api.useLazyGetSettingsQuery();
    const [getSettingsSchema, { error: errorSettingsSchema }] = api.useLazyGetSettingsSchemaQuery();

    useErrorHandler({
        error: errorSettings,
        message: 'Error while fetching settings data'
    });

    useErrorHandler({
        error: errorSettingsSchema,
        message: 'Error while fetching settings schema'
    });

    useEffect(() => {
        getSettingsSchema({});
        getSettings({});
    }, [getSettings, getSettingsSchema]);

    if (isObjectEmpty(settingsFields) || isObjectEmpty(settingsFieldsSchema))
        return <div><h1>Loading...</h1></div>;

    return (
        <SettingsForm fields={settingsFields} fieldsSchema={settingsFieldsSchema}/>
        // <Form schema={settingsFieldsSchema['cloud']} validator={validator} formData={settingsFields['cloud']}/>
    );
};

export default Settings;