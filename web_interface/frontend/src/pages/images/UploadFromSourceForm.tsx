import {Box} from "@mui/material";
import {Form} from "@rjsf/mui";
import validator from "@rjsf/validator-ajv8";
import {RJSFSchema} from "@rjsf/utils";
import {useState} from "react";
import useNewImageMutation from "./helpers/useNewImageMutation";

const schema = {
    title: "Upload image from the web",
    description: "Paste the link to the image below to upload it to images",
    type: "object",
    required: ["link"],
    properties: {
        link: {
            type: "string",
            title: "Link to the image",
            format: "uri"
        }
    }
};

interface UploadFromSourceFormProps {
    imageId: string;
}

const UploadFromSourceForm = ({imageId}: UploadFromSourceFormProps) => {
    const [formData, setFormData] = useState({link: ''});

    const { mutationTrigger: newImageMutation } = useNewImageMutation();

    const onChange = (e: any) => setFormData(e.formData);
    const onSubmit = () => {
        formData.link && imageId && newImageMutation({id: imageId, url: formData.link})
    };

    return (
        <Box style={{padding: '2em'}}>
            <Form
                schema={schema as RJSFSchema}
                formData={formData}
                validator={validator}
                onChange={onChange}
                onSubmit={onSubmit}
            />
        </Box>
    );
};

export default UploadFromSourceForm;