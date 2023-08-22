import {Box, Button} from "@mui/material";
import {Form} from "@rjsf/mui";
import validator from "@rjsf/validator-ajv8";
import {useAppDispatch, useAppSelector} from "../../app/hooks";
import {changeFields, selectSettingsFieldsAreChanged} from "../../app/slices/settingsSlice";
import {IChangeEvent} from "@rjsf/core";
import useUpdateSettings from "./helpers/useUpdateSettings";
import useResetSettings from "./helpers/useResetSettings";
import SettingsFormGroup, { formGroupClassNames } from "./SettingsFormGroup";

interface FormProps {
    fields: {
        [key: string]: any
    };
    fieldsSchema: {
        [key: string]: any
    };
}

const SettingsForm = ({fields, fieldsSchema}: FormProps) => {
    const dispatch = useAppDispatch();
    const fieldsAreChanged = useAppSelector(selectSettingsFieldsAreChanged);

    const { updateSettings } = useUpdateSettings();
    const { resetSettings } = useResetSettings();

    const onChange = (e: IChangeEvent<any>) => {
        dispatch(changeFields(e.formData));
    };

    const onSubmit = () => { updateSettings({fields}); };
    const onReset = () => { resetSettings({}) };

    const uiSchema = Object.keys(fieldsSchema.properties).reduce((acc: any, key: string) => {
        acc[key] = { "ui:classNames": formGroupClassNames };
        return acc;
    }, {});
    uiSchema.description.gpt_settings = {prompt: {
            "ui:widget": "textarea",
            "ui:options": { "rows": 10 }
        }
    };

    return (
        <Box style={{display: 'flex', gap: '2em'}}>
            <Box
                style={{flex: 1, height: '87vh', overflow: 'auto'}}
            >
                <Form
                    schema={fieldsSchema}
                    uiSchema={uiSchema}
                    validator={validator}
                    formData={fields}
                    onChange={onChange}
                    templates={{ FieldTemplate: SettingsFormGroup }}
                >
                    <Button disabled/>
                </Form>
            </Box>
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
