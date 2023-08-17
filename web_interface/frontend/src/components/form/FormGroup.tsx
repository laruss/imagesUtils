import {FormControl, Paper, TextField, Typography} from "@mui/material";
import {determineType} from "../../helpers/methods";
import BooleanDropdown from "./BooleanDropdown";

interface FormGroupProps {
    name: string;
    fields: {
        [key: string]: any
    }
}

const FormGroup = ({name, fields}: FormGroupProps) => {
    const randomKey = () => (Math.random() + 1).toString(36).substring(7);

    const multilineFields = ['default_prompt', 'gptText'];

    return (
        <Paper style={{ padding: 20, marginBottom: 20 }}>
            <FormControl component='fieldset'>
                <Typography variant="h6">{name}</Typography>
                {
                    Object.keys(fields).map((field, index) => {
                        const fieldType = determineType(fields[field]);

                        if (fieldType === 'object' || fieldType === 'array') {
                            return (
                                <FormGroup
                                    key={randomKey()}
                                    name={field}
                                    fields={fields[field]}
                                />
                            )
                        }

                        if (fieldType === 'boolean') {
                            return (
                                <BooleanDropdown
                                    key={randomKey()}
                                    label={field}
                                    onChange={() => {}}
                                    value={fields[field]}
                                />
                            )
                        }

                        if (fieldType === 'string' || fieldType === 'number') {
                            return (
                                <TextField
                                    fullWidth
                                    key={randomKey()}
                                    label={field}
                                    type={fieldType === 'string' ? 'text' : 'number'}
                                    sx={{ margin: 1, width: '25ch' }}
                                    variant="standard"
                                    multiline={multilineFields.includes(field)}
                                    value={fields[field]}
                                />
                            )
                        }

                        return null;
                    })
                }
            </FormControl>
        </Paper>
  );
};

export default FormGroup;