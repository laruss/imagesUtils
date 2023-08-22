import {Box} from "@mui/material";
import ActionButton, {ActionButtonProps} from "./ActionButton";
import {api} from "../../app/api";
import {MutationTrigger} from "@reduxjs/toolkit/dist/query/react/buildHooks";
import ActionsDropdown, {ActionsDropdownProps} from "./ActionsDropdown";

const ImagesActions = () => {
    const onClick = (mutationTrigger: MutationTrigger<any>) => mutationTrigger({});

    const actions: (ActionButtonProps | ActionsDropdownProps)[] = [
        {
            onClick,
            label: 'download images',
            apiMutation: api.useDownloadImagesMutation,
            color: 'primary'
        },
        {
            label: 'descriptions',
            buttons: [
                {
                    onClick,
                    label: 'generate',
                    apiMutation: api.useDescribeImagesDescribeMutation,
                    color: 'info'
                },
                {
                    onClick,
                    label: 'delete nsfw',
                    apiMutation: api.useDescribeImagesDeleteNSFWMutation,
                    color: 'error'
                },
                {
                    onClick,
                    label: 'process by gpt',
                    apiMutation: api.useDescribeImagesGptMutation,
                    color: 'info'
                },
                {
                    onClick,
                    label: 'gpt to json',
                    apiMutation: api.useDescribeImagesGptJsonMutation,
                    color: 'info'
                }
            ]
        },
        {
            label: 'optimization',
            buttons: [
                {
                    onClick,
                    label: 'convert to webp',
                    apiMutation: api.useOptimizeImagesWebPMutation,
                    color: 'info'
                },
                {
                    onClick,
                    label: 'cartoonize',
                    apiMutation: api.useOptimizeImagesCartoonizeMutation,
                    color: 'info'
                },
                {
                    onClick,
                    label: 'minimize',
                    apiMutation: api.useOptimizeImagesMinimizeMutation,
                    color: 'info'
                },
                {
                    onClick,
                    label: 'delete duplicates',
                    apiMutation: api.useOptimizeImagesDuplicatesMutation,
                }
            ]
        },
        {
            label: 'cloud',
            buttons: [
                {
                    onClick,
                    label: 'upload all',
                    apiMutation: api.useCloudUploadMutation,
                    color: 'info'
                },
                {
                    onClick,
                    label: 'download all',
                    apiMutation: api.useCloudDownloadMutation,
                    color: 'info'
                }
            ]
        }
    ];

    return (
        <Box style={{
            position: "fixed",
            left: '50%', right: '50%',
            top: '1ch', display: 'inline-flex', justifyContent: 'center',
        }}>
            {
                actions.map((action, index) => (
                    action.label === actions[0].label ?
                        <ActionButton key={index} {...(action as ActionButtonProps)}/> :
                        <ActionsDropdown key={index} {...(action as ActionsDropdownProps)}/>
                ))
            }
        </Box>
    );
};

export default ImagesActions;