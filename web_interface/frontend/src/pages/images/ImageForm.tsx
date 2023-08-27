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
import ArrayField from "../../components/form/ArrayField";

interface ImageFormProps {
    imageId: string;
    newImage: null | string;
}

const ImageForm = ({imageId, newImage}: ImageFormProps) => {
    const dispatch = useAppDispatch();

    useGetImageData({imageId, newImage});

    const imageDataSchema = useAppSelector(selectImageDataSchema);
    const currentImageData = useAppSelector(selectChangedImageData);
    const dataIsChanged = useAppSelector(selectDataIsChanged);

    const {updateImageData} = useUpdateImageData();

    const onChange = (e: IChangeEvent<any>) => dispatch(changeImageData(e.formData));
    const onSubmit = () => { updateImageData({id: imageId, data: currentImageData}); };

    const fields = { ArrayField };

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
                disabled={Boolean(newImage)}
                fields={fields}
            >
                <Button disabled/>
            </Form>
            <Button
                variant={'contained'}
                style={{position: "absolute", top: '1ch', right: '1ch'}}
                disabled={!dataIsChanged || Boolean(newImage)}
                onClick={onSubmit}
                color={'error'}
            >
                Save
            </Button>
        </Box>
    );
};

export default ImageForm;