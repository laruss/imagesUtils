import {ImagesState} from "../../types/redux";
import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {api} from "../api";

const initialState: ImagesState = {
    images: [],
    currentImage: null,
    currentImageData: {}
};

export const imagesSlice = createSlice({
    name: 'images',
    initialState,
    reducers: {
        setCurrentImage: (state, action: PayloadAction<string | null>) => {
            state.currentImage = action.payload;
        }
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
            }
        )
    }
});

export const {
    setCurrentImage
} = imagesSlice.actions;

export default imagesSlice.reducer;

export const selectImages = (state: any) => state.images.images;

export const selectCurrentImage = (state: any) => state.images.currentImage;

export const selectCurrentImageData = (state: any) => state.images.currentImageData;