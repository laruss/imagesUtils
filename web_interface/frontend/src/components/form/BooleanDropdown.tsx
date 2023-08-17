import Dropdown from "./Dropdown";

interface BooleanDropdownProps {
    label: string;
    value: boolean;
    onChange: (event: any) => void;
}

const BooleanDropdown = ({label, value, onChange}: BooleanDropdownProps) => {
    const strValue = String(value);
    const values = [
        {
            label: 'true',
            value: 'true'
        },
        {
            label: 'false',
            value: 'false'
        }
    ];

    return (
        <Dropdown label={label} onChange={() => {}} selected={{label: strValue, value: strValue}} values={values}/>
    );
};

export default BooleanDropdown;