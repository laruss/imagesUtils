import {Box, Button} from "@mui/material";
import {Form} from "@rjsf/mui";
import validator from "@rjsf/validator-ajv8";
import {useAppDispatch, useAppSelector} from "../../app/hooks";
import {changeFields, selectSettingsFieldsAreChanged} from "../../app/slices/settingsSlice";
import {IChangeEvent} from "@rjsf/core";
import {api} from "../../app/api";
import useErrorHandler from "../../helpers/useErrorHandler";
import {useEffect} from "react";
import {showLoader, showNotification} from "../../helpers/dispatchers";

interface FormProps {
    fields: {
        [key: string]: any
    };
    fieldsSchema: {
        [key: string]: {
            [key: string]: any;
        }
    };
}

const SettingsForm = ({fields, fieldsSchema}: FormProps) => {
    const dispatch = useAppDispatch();
    const fieldsAreChanged = useAppSelector(selectSettingsFieldsAreChanged);

    const onChange = (e: IChangeEvent<any>, key: string) => {
        const newFields = {...fields};
        newFields[key] = e.formData;
        dispatch(changeFields(newFields));
    };

    const [
        updateSettings,
        { error, data, isLoading }
    ] = api.useUpdateSettingsMutation();

    const onSubmit = () => { updateSettings({fields}); };

    useErrorHandler({ error, message: `Error while updating settings` });

    useEffect(() => {
        if (data) showNotification(`Settings updated`, 'success');
    }, [data]);

    useEffect(() => showLoader(isLoading), [isLoading]);

    return (
        <Box style={{display: 'flex', gap: '2em'}}>
            {
                Object.keys(fieldsSchema).map((key, index) => {
                    return (
                        <Box
                            key={index}
                            style={{flex: 1, height: '87vh', overflow: 'auto'}}
                        >
                            <Form
                                schema={fieldsSchema[key]}
                                validator={validator}
                                formData={fields[key]}
                                onChange={(e) => onChange(e, key)}
                            >
                                <Button disabled/>
                            </Form>
                        </Box>
                    )
                })
            }
            <Button
                variant={'contained'}
                style={{position: "absolute", top: '1ch', right: '1ch'}}
                disabled={!fieldsAreChanged}
                onClick={onSubmit}
            >
                Save
            </Button>
        </Box>
    );
};

export default SettingsForm;
