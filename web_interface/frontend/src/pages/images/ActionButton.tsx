import {Button} from "@mui/material";
import {api} from "../../app/api";
import useErrorHandler from "../../helpers/useErrorHandler";
import {useEffect} from "react";
import {showLoader, showNotification} from "../../helpers/dispatchers";

export interface ActionButtonProps {
    image: string;
    label: string;
    apiMutation: typeof api.useUpdateImageDescriptionMutation
        | typeof api.useUpdateByGPTMutation
        | typeof api.useSetJSONFromGPTMutation
        | typeof api.useConvertToWebPMutation
        | typeof api.useOptimizeImageMutation
        | typeof api.useDeleteImageMutation;
    color?: "inherit" | "error" | "primary" | "secondary" | "success" | "info" | "warning" | undefined;
    method?: () => void;
}

const ActionButton = ({image, label, apiMutation, color, method}: ActionButtonProps) => {
    const [
        mutationTrigger,
        { error, data, isLoading }
    ] = apiMutation();

    useErrorHandler({ error, message: `Error while ${label}` });

    useEffect(() => {
        if (data) {
            showNotification(`${label} done`, 'success');
            method && method();
        }
    }, [data]);

    useEffect(() => showLoader(isLoading), [isLoading]);

    const onClick = () => mutationTrigger({id: image});

    return (
        <Button
            variant={'contained'}
            onClick={onClick}
            color={color}
        >
            {label}
        </Button>
    );
};

export default ActionButton;