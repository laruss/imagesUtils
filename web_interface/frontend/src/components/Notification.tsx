import * as React from 'react';
import Stack from '@mui/material/Stack';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert, { AlertProps } from '@mui/material/Alert';
import {useAppDispatch, useAppSelector} from "../app/hooks";
import {setNotification} from "../app/slices/appSlice";

const Alert = React.forwardRef<HTMLDivElement, AlertProps>(function Alert(
    props,
    ref,
) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

export default function Notification() {
    const dispatch = useAppDispatch();
    const {isOpen, text, variant} = useAppSelector(state => state.app.notification);

    const handleClose = (event?: React.SyntheticEvent | Event, reason?: string) => {
        if (reason === 'clickaway') {
            return;
        }

        dispatch(setNotification({isOpen: false, text: '', variant: 'info'}));
    };

    return (
        <Stack spacing={2} sx={{ width: '100%' }}>
            <Snackbar
                open={isOpen}
                autoHideDuration={6000}
                onClose={handleClose}
                anchorOrigin={{vertical: 'top', horizontal: 'right'}}
            >
                <Alert
                    onClose={handleClose}
                    severity={variant}
                    sx={{ width: '100%' }}
                >
                    {text}
                </Alert>
            </Snackbar>
        </Stack>
    );
}
