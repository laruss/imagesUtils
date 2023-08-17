import {FormControl, Paper, TextField, Typography} from "@mui/material";
import FormGroup from "../../components/form/FormGroup";

interface FormProps {
    fields: {
        [key: string]: any
    };
}

const Form = ({fields}: FormProps) => {
    return (
        <div>
            <form style={{display: 'flex'}}>
                {
                    Object.keys(fields).map((field, index) => (
                        <FormGroup name={field} fields={fields[field]} key={index}/>
                    ))
                }
            </form>
        </div>
    );
};

export default Form;