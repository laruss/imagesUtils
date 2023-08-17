import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from '@reduxjs/toolkit';

import { AppState } from "../../types/redux";

const initialState: AppState = {
    isLoaderShown: false,
    notification: {
        isOpen: false,
        text: '',
        variant: 'info'
    }
};

export const appSlice = createSlice({
    name: 'app',
    initialState,
    reducers: {
        setNotification: (state, action: PayloadAction<AppState['notification']>) => {
            state.notification = action.payload;
        },
        setLoaderShown: (state, action: PayloadAction<boolean>) => {
            state.isLoaderShown = action.payload;
        },
    },
    extraReducers: builder => {

    }
});

export const {
    setNotification,
    setLoaderShown
} = appSlice.actions;

export default appSlice.reducer;

export const selectIsLoaderShown = (state: any) => state.app.isLoaderShown;