import {Button, MenuItem} from "@mui/material";
import {MutationTrigger, UseMutation} from "@reduxjs/toolkit/dist/query/react/buildHooks";
import {MutationDefinition} from "@reduxjs/toolkit/query";
import useImageDataMutation from "./helpers/useImageDataMutation";

export interface ActionButtonProps {
    label: string;
    apiMutation: UseMutation<MutationDefinition<any, any, any, any, any>>;
    color?: "inherit" | "error" | "primary" | "secondary" | "success" | "info" | "warning" | undefined;
    mutationCallBack?: () => void;
    onClick: (mutationTrigger: MutationTrigger<any>) => void;
    asMenuItem?: boolean;
}

const ActionButton = ({label, apiMutation, color, mutationCallBack, onClick, asMenuItem}: ActionButtonProps) => {

    const {mutationTrigger} = useImageDataMutation({
        apiMutationMethod: apiMutation,
        actionName: label,
        callback: mutationCallBack
    });

    return (
        asMenuItem ?
            <MenuItem onClick={() => onClick(mutationTrigger)} color={color}>{label}</MenuItem> :
            <Button
                variant={'contained'}
                onClick={() => onClick(mutationTrigger)}
                color={color}
                style={{zIndex: 5, flexShrink: 0}}
            >
                {label}
            </Button>
    );
};

export default ActionButton;