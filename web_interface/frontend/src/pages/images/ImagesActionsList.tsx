import Divider from "@mui/material/Divider";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import * as React from "react";
import {Box} from "@mui/material";

const ImagesActionsList = () => {
    return (
        <Box>
            <Divider>Actions</Divider>
            <List component="nav" aria-label="secondary mailbox folders">
                <ListItemButton
                    selected={false}
                    onClick={(event) => {}}
                >
                    <ListItemText primary="Trash" />
                </ListItemButton>
                <ListItemButton
                    selected={false}
                    onClick={(event) => {}}
                >
                    <ListItemText primary="Spam" />
                </ListItemButton>
            </List>
        </Box>
    );
};

export default ImagesActionsList;