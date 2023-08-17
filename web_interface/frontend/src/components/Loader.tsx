import {useAppSelector} from "../app/hooks";
import {selectIsLoaderShown} from "../app/slices/appSlice";
import {Box, CircularProgress, Modal} from "@mui/material";

const style = {
    position: 'absolute' as 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    boxShadow: 24,
    p: 4,
};

const Loader = () => {
    const isLoaderShown = useAppSelector(selectIsLoaderShown);

    return (
        <Modal open={isLoaderShown}>
            <Box sx={style}><CircularProgress size={60}/></Box>
        </Modal>
    );
};

export default Loader;