import {Box} from "@mui/material";
import {api} from "../../app/api";
import ActionButton, {ActionButtonProps} from "./ActionButton";
import {useAppDispatch} from "../../app/hooks";
import {setCurrentImage} from "../../app/slices/imagesSlice";
import {MutationTrigger} from "@reduxjs/toolkit/dist/query/react/buildHooks";

interface ImageActionsProps {
    image: string;
    newImage: null | string;
}

const OneImageActions = ({image, newImage}: ImageActionsProps) => {
    const dispatch = useAppDispatch();

    const onClick = (mutationTrigger: MutationTrigger<any>) => mutationTrigger({id: image});

    const buttons: ActionButtonProps[] = [
        {
            onClick,
            label: 'generate description',
            apiMutation: api.useUpdateImageDescriptionMutation,
            color: 'primary',
            disabled: Boolean(newImage)
        },
        {
            onClick,
            label: 'process by gpt',
            apiMutation: api.useUpdateByGPTMutation,
            color: 'info',
            disabled: Boolean(newImage)
        },
        {
            onClick,
            label: 'gpt to json',
            apiMutation: api.useSetJSONFromGPTMutation,
            color: 'primary',
            disabled: Boolean(newImage)
        },
        {
            onClick,
            label: 'to webp',
            apiMutation: api.useConvertToWebPMutation,
            color: 'info',
            disabled: Boolean(newImage)
        },
        {
            onClick,
            label: 'optimize size',
            apiMutation: api.useOptimizeImageMutation,
            color: 'primary',
            disabled: Boolean(newImage)
        },
        {
            onClick,
            label: 'cartoonize',
            apiMutation: api.useCartoonizeImageMutation,
            color: 'info',
            disabled: Boolean(newImage)
        },
        {
            onClick,
            label: 'delete',
            apiMutation: api.useDeleteImageMutation,
            color: 'error',
            mutationCallBack: () => { dispatch(setCurrentImage(null)) },
            disabled: Boolean(newImage)
        }
    ];

    return (
        <Box style={{
            position: 'fixed',
            bottom: 0,
            left: 0,
            zIndex: 5,
            display: 'inline-flex',
            width: '100vw',
            justifyContent: 'center'
        }}>
            {
                buttons.map((button, index) => (
                    <ActionButton key={index} {...button}/>
                ))
            }
        </Box>
    );
};

export default OneImageActions;