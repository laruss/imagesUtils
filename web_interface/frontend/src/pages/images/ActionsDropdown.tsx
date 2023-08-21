import {Box, Button, Menu, MenuItem} from "@mui/material";
import React from "react";
import ActionButton, {ActionButtonProps} from "./ActionButton";

export interface ActionsDropdownProps {
    label: string;
    buttons: ActionButtonProps[];
}

const ActionsDropdown = ({label, buttons}: ActionsDropdownProps) => {
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
    const open = Boolean(anchorEl);
    const handleClick = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <Box style={{display: 'flex'}}>
            <Button
                id="demo-positioned-button"
                aria-controls={open ? 'demo-positioned-menu' : undefined}
                aria-haspopup="true"
                aria-expanded={open ? 'true' : undefined}
                onClick={handleClick}
                variant={'contained'}
                style={{zIndex: 5, flexShrink: 0, margin: '0 1em'}}
            >
                {`${label} ▼`}
            </Button>
            <Menu
                id="demo-positioned-menu"
                aria-labelledby="demo-positioned-button"
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'left',
                }}
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'left',
                }}
            >
                {
                    buttons.map((button, index) =>
                        <ActionButton key={index} asMenuItem={true} {...button}/>
                    )
                }
            </Menu>
        </Box>
    );
};

export default ActionsDropdown;