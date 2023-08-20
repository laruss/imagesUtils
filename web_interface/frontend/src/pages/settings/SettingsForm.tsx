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
import useUpdateSettings from "./helpers/useUpdateSettings";
import useResetSettings from "./helpers/useResetSettings";

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

    const { updateSettings } = useUpdateSettings();
    const { resetSettings } = useResetSettings();

    const onChange = (e: IChangeEvent<any>, key: string) => {
        const newFields = {...fields};
        newFields[key] = e.formData;
        dispatch(changeFields(newFields));
    };

    const onSubmit = () => { updateSettings({fields}); };
    const onReset = () => { resetSettings({}); };

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
            <Box
                style={{position: "absolute", top: '1ch', right: '1ch', display: 'flex', gap: '0.5em'}}
            >
                <Button
                    variant={'contained'}
                    onClick={onReset}
                >
                    Reset
                </Button>
                <Button
                    variant={'contained'}
                    disabled={!fieldsAreChanged}
                    onClick={onSubmit}
                >
                    Save
                </Button>
            </Box>
        </Box>
    );
};

export default SettingsForm;
