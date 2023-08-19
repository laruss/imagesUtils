import {Box, Button} from "@mui/material";
import {useAppDispatch, useAppSelector} from "../../app/hooks";
import {
    changeImageData,
    selectChangedImageData,
    selectDataIsChanged,
    selectImageDataSchema
} from "../../app/slices/imagesSlice";
import {Form} from "@rjsf/mui";
import validator from "@rjsf/validator-ajv8";
import {IChangeEvent} from "@rjsf/core";
import useUpdateImageData from "./helpers/useUpdateImageData";
import useGetImageData from "./helpers/useGetImageData";

interface ImageFormProps {
    imageId: string;
}

const ImageForm = ({imageId}: ImageFormProps) => {
    const dispatch = useAppDispatch();

    useGetImageData(imageId);

    const imageDataSchema = useAppSelector(selectImageDataSchema);
    const currentImageData = useAppSelector(selectChangedImageData);
    const dataIsChanged = useAppSelector(selectDataIsChanged);

    const {updateImageData} = useUpdateImageData();

    const onChange = (e: IChangeEvent<any>) => dispatch(changeImageData(e.formData));
    const onSubmit = () => { updateImageData({id: imageId, data: currentImageData}); };

    if (!imageDataSchema || !currentImageData) return null;

    return (
        <Box
            style={{flex: 1, height: '87vh', overflow: 'auto'}}
        >
            <Form
                schema={imageDataSchema}
                validator={validator}
                formData={currentImageData}
                onChange={onChange}
            >
                <Button disabled/>
            </Form>
            <Button
                variant={'contained'}
                style={{position: "absolute", top: '1ch', right: '1ch'}}
                disabled={!dataIsChanged}
                onClick={onSubmit}
                color={'error'}
            >
                Save
            </Button>
        </Box>
    );
};

export default ImageForm;