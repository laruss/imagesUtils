import {FormControl, InputLabel, MenuItem, Select} from "@mui/material";
import {DropdownValueType} from "../../types/components";

interface DropdownProps {
    label: string;
    onChange: (event: any) => void;
    selected: DropdownValueType;
    values: DropdownValueType[];
}

const Dropdown = ({label, values, selected, onChange}: DropdownProps) => {
    return (
        // eslint-disable-next-line react/jsx-no-undef
        <FormControl fullWidth style={{padding: '1em 0'}}>
            <InputLabel id="demo-simple-select-label">{label}</InputLabel>
            <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={selected.value}
                label="Age"
                onChange={onChange}
            >
                {
                    values && values.map((value, index) => {
                        return <MenuItem key={index} value={value.value}>{value.label}</MenuItem>
                    })
                }
            </Select>
        </FormControl>
    );
};

export default Dropdown;