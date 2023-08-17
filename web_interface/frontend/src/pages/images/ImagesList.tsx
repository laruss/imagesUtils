import * as React from 'react';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import {Paper} from "@mui/material";
import Divider from "@mui/material/Divider";
import {useAppDispatch, useAppSelector} from "../../app/hooks";
import {selectCurrentImage, selectImages, setCurrentImage} from "../../app/slices/imagesSlice";
import ImagesActionsList from "./ImagesActionsList";

export default function ImagesList() {
    const dispatch = useAppDispatch();
    const images = useAppSelector(selectImages);
    const currentImage = useAppSelector(selectCurrentImage);

    const handleListItemClick = (
        event: React.MouseEvent<HTMLDivElement, MouseEvent>,
        index: string,
    ) => {
        dispatch(setCurrentImage(index));
    };

    if (!images)
        return <div><h1>Loading...</h1></div>;

    return (
        <Box sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
            <Paper style={{ padding: 20, marginBottom: 20, height: '80vh' }}>
                <Divider>Images</Divider>
                <List component="nav" aria-label="main mailbox folders" style={{height: '60vh', overflow: 'auto'}}>
                    {
                        images && images.map((image: string) => {
                            return (
                                <ListItemButton
                                    key={image}
                                    selected={currentImage === image}
                                    onClick={(event) => handleListItemClick(event, image)}
                                >
                                    <ListItemIcon>
                                    </ListItemIcon>
                                    <ListItemText primary={image} />
                                </ListItemButton>
                            )
                        })
                    }
                </List>
                <ImagesActionsList/>
            </Paper>
        </Box>
    );
}