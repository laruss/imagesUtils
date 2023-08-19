import {Box, Paper} from "@mui/material";
import ActionButton, {ActionButtonProps} from "./ActionButton";
import {api} from "../../app/api";
import {MutationTrigger} from "@reduxjs/toolkit/dist/query/react/buildHooks";

const ImagesActions = () => {
    const onClick = (mutationTrigger: MutationTrigger<any>) => mutationTrigger({});

    const buttons: ActionButtonProps[] = [
        {
            onClick,
            label: 'download images',
            apiMutation: api.useDownloadImagesMutation,
            color: 'primary'
        },
        {
            onClick,
            label: 'generate descriptions',
            apiMutation: api.useGenerateDescriptionsMutation,
            color: 'info'
        },
        {
            onClick,
            label: 'optimize images',
            apiMutation: api.useOptimizeImagesMutation,
            color: 'primary'
        },
        {
            onClick,
            label: 'use cloud',
            apiMutation: api.useUseCloudMutation,
            color: 'info'
        }
    ];

    return (
        <Box style={{
            position: "fixed",
            left: '50%', right: '50%',
            top: '1ch', display: 'inline-flex', justifyContent: 'center',
        }}>
            {
                buttons.map((button, index) => (
                    <ActionButton key={index} {...button}/>
                ))
            }
        </Box>
    );
};

export default ImagesActions;