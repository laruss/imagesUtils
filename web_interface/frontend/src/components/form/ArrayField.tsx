import {FieldProps} from "@rjsf/utils";
import {
    OutlinedInput,
    InputLabel,
    MenuItem,
    Select,
    FormControl, Chip, Tooltip
} from "@mui/material";
import Stack from "@mui/material/Stack";
import CancelIcon from "@mui/icons-material/Cancel";
import CheckIcon from "@mui/icons-material/Check";
import {getMultiSelectItems} from "./helpers";

const ArrayField = (props: FieldProps) => {
    const items = getMultiSelectItems(props) as string[];
    const selectedItems: string[] | undefined = props.formData as string[];

    if (!items || selectedItems === undefined) return null;

    return (
        <FormControl sx={{ m: 1, width: 500 }}>
            <InputLabel>{props.name.toUpperCase()}</InputLabel>
            <Select
                multiple
                disabled={props.disabled}
                value={selectedItems || []}
                onChange={(e) => props.onChange(e.target.value as string[])}
                input={<OutlinedInput label="Multiple Select" />}
                renderValue={(selected) => (
                    <Stack gap={1} direction="row" flexWrap="wrap">
                        {selected.map((value) => (
                            <Tooltip title={value} key={value}>
                                <Chip
                                    label={value}
                                    style={{ maxWidth: 100 }}
                                    onDelete={() =>
                                        props.onChange(
                                            selectedItems.filter((item) => item !== value)
                                        )
                                    }
                                    deleteIcon={
                                        <CancelIcon
                                            onMouseDown={(event) => event.stopPropagation()}
                                        />
                                    }
                                />
                            </Tooltip>
                        ))}
                    </Stack>
                )}
            >
                {items.map((name) => (
                    <MenuItem
                        key={name}
                        value={name}
                        sx={{ justifyContent: "space-between" }}
                    >
                        {name}
                        {selectedItems.includes(name) ? <CheckIcon color="info" /> : null}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
    )
};

export default ArrayField;