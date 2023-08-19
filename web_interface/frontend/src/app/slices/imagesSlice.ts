import {ImagesState} from "../../types/redux";
import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {api} from "../api";
import {areObjectsEqual} from "../../helpers/methods";

const initialState: ImagesState = {
    images: [],
    imageDataSchema: {},
    currentImage: null,
    currentImageData: {},
    changedImageData: {},
    dataIsChanged: false,
    dataIsValid: true, // TODO
};

export const imagesSlice = createSlice({
    name: 'images',
    initialState,
    reducers: {
        setCurrentImage: (state, action: PayloadAction<string | null>) => {
            state.currentImage = action.payload;
            state.changedImageData = {};
            state.dataIsChanged = false;
            state.dataIsChanged = false;
        },
        changeImageData: (state, action: PayloadAction<ImagesState['changedImageData']>) => {
            state.dataIsChanged = !areObjectsEqual(state.currentImageData, action.payload);
            state.changedImageData = action.payload;
        },
    },
    extraReducers: builder => {
        builder.addMatcher(
            api.endpoints.getImages.matchFulfilled,
            (state, {payload}) => {
                state.images = payload;
            }
        ).addMatcher(
            api.endpoints.getImageData.matchFulfilled,
            (state, {payload, meta}) => {
                state.currentImageData = payload;
                state.changedImageData = payload;
                state.dataIsChanged = false;
            }
        ).addMatcher(
            api.endpoints.getImageDataSchema.matchFulfilled,
            (state, {payload}) => {
                state.imageDataSchema = payload;
            }
        )
    }
});

export const {
    setCurrentImage,
    changeImageData
} = imagesSlice.actions;

export default imagesSlice.reducer;

export const selectImages = (state: any) => state.images.images;

export const selectImageDataSchema = (state: any) => state.images.imageDataSchema;

export const selectCurrentImage = (state: any) => state.images.currentImage;

export const selectCurrentImageData = (state: any) => state.images.currentImageData;

export const selectChangedImageData = (state: any) => state.images.changedImageData;

export const selectDataIsChanged = (state: any) => state.images.dataIsChanged;