import {useState} from "react";
import {FieldTemplateProps} from "@rjsf/utils";
import {Typography} from "@mui/material";

export const formGroupClassNames = 'form-group-toggle';

const SettingsFormGroup = (props: FieldTemplateProps) => {
    const [isOpen, setIsOpen] = useState(false);
    const isToggle = props.classNames?.includes(formGroupClassNames);

    const onClick = () => {
        !isOpen && props.classNames?.includes(formGroupClassNames) && setIsOpen(!isOpen);
    };

    return (
        <div onClick={onClick}>
            {isToggle && !isOpen && <Typography style={{cursor: 'pointer'}} variant={'h5'}>{props.label} ▼</Typography>}
            <div style={{display: (isOpen || !isToggle) ? 'block': 'none'}}>
                {props.children}
            </div>
        </div>
    )
};

export default SettingsFormGroup;