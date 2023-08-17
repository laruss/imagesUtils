import {Paper} from "@mui/material";
import {api} from "../../app/api";
import ActionButton, {ActionButtonProps} from "./ActionButton";
import {useAppDispatch} from "../../app/hooks";
import {setCurrentImage} from "../../app/slices/imagesSlice";

interface ImageActionsProps {
    image: string;
}

const ImageActions = ({image}: ImageActionsProps) => {
    const dispatch = useAppDispatch();

    const buttons: ActionButtonProps[] = [
        {
            image,
            label: 'generate description',
            apiMutation: api.useUpdateImageDescriptionMutation,
            color: 'primary'
        },
        {
            image,
            label: 'process by gpt',
            apiMutation: api.useUpdateByGPTMutation,
            color: 'info'
        },
        {
            image,
            label: 'gpt to json',
            apiMutation: api.useSetJSONFromGPTMutation,
            color: 'primary'
        },
        {
            image,
            label: 'to webp',
            apiMutation: api.useConvertToWebPMutation,
            color: 'info'
        },
        {
            image,
            label: 'optimize size',
            apiMutation: api.useOptimizeImageMutation,
            color: 'primary'
        },
        {
            image,
            label: 'delete',
            apiMutation: api.useDeleteImageMutation,
            color: 'error',
            method: () => { dispatch(setCurrentImage(null)) }
        }
    ]

    return (
        <Paper style={{paddingTop: '1em'}}>
            {
                buttons.map((button, index) => (
                    <ActionButton key={index} {...button}/>
                ))
            }
        </Paper>
    );
};

export default ImageActions;