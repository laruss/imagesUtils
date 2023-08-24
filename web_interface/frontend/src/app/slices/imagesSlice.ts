import {ImagesState} from "../../types/redux";
import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {api} from "../api";
import {areObjectsEqual, getUniqueId} from "../../helpers/methods";

const initialState: ImagesState = {
    images: [],
    imageDataSchema: {},
    currentImage: null,
    currentImageData: {},
    changedImageData: {},
    dataIsChanged: false,
    dataIsValid: true, // TODO
    newImage: null,
};

export const imagesSlice = createSlice({
    name: 'images',
    initialState,
    reducers: {
        setCurrentImage: (state, action: PayloadAction<string | null>) => {
            if (action.payload === state.currentImage) return state;
            const images = [...state.images];
            state.newImage && images.pop();
            return {
                ...state,
                images,
                currentImage: action.payload,
                currentImageData: {},
                changedImageData: {},
                dataIsChanged: false,
                dataIsValid: true,
                newImage: null,
            }
        },
        changeImageData: (state, action: PayloadAction<ImagesState['changedImageData']>) => {
            state.dataIsChanged = !areObjectsEqual(state.currentImageData, action.payload);
            state.changedImageData = action.payload;
        },
        addEmptyImage: (state, action) => {
            const uniqueId = getUniqueId(state.images);
            return {
                ...state,
                images: [...state.images, uniqueId],
                currentImage: uniqueId,
                currentImageData: {},
                changedImageData: {},
                dataIsChanged: false,
                dataIsValid: true,
                newImage: uniqueId,
            };
        },
    },
    extraReducers: builder => {
        builder.addMatcher(
            api.endpoints.getImages.matchFulfilled,
            (state, {payload}) => {
                if (state.newImage && !payload.includes(state.newImage)) return;
                state.images = payload;
                state.newImage = null;
            }
        ).addMatcher(
            api.endpoints.getImageData.matchFulfilled,
            (state, {payload, meta}) => {
                if (state.newImage) return;

                state.currentImageData = payload;
                state.changedImageData = payload;
                state.dataIsChanged = false;
                state.dataIsValid = true;
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
    changeImageData,
    addEmptyImage
} = imagesSlice.actions;

export default imagesSlice.reducer;

export const selectImages = (state: any) => state.images.images;
export const selectImageDataSchema = (state: any) => state.images.imageDataSchema;
export const selectCurrentImage = (state: any) => state.images.currentImage;
export const selectCurrentImageData = (state: any) => state.images.currentImageData;
export const selectChangedImageData = (state: any) => state.images.changedImageData;
export const selectDataIsChanged = (state: any) => state.images.dataIsChanged;
export const selectDataIsValid = (state: any) => state.images.dataIsValid;
export const selectNewImage = (state: any) => state.images.newImage;