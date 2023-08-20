import * as React from 'react';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import {ListItem, Paper} from "@mui/material";
import Divider from "@mui/material/Divider";
import {useAppDispatch, useAppSelector} from "../../app/hooks";
import {selectCurrentImage, selectImages, setCurrentImage} from "../../app/slices/imagesSlice";
import ImagesActions from "./ImagesActions";

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
                <List component="nav" aria-label="main mailbox folders" style={{height: '76vh', overflow: 'auto'}}>
                    {
                        images && (
                            images.length > 0 ? (
                                images.map((image: string) => {
                                    return (
                                        <ListItem key={image}>
                                            <ListItemButton
                                                key={image}
                                                selected={currentImage === image}
                                                onClick={(event) => handleListItemClick(event, image)}
                                            >
                                                <ListItemText primary={image}/>
                                            </ListItemButton>
                                        </ListItem>
                                    )
                                })
                            ) : (
                                <Box>
                                    <h1>No images</h1>
                                </Box>
                            )
                        )
                    }
                </List>
            </Paper>
            <ImagesActions/>
        </Box>
    );
}