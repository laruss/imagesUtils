import {SettingsState} from "../../types/redux";
import {createSlice} from "@reduxjs/toolkit";
import {api} from "../api";

const initialState: SettingsState = {
    fields: {}
};

export const settingsSlice = createSlice({
    name: 'settings',
    initialState,
    reducers: {

    },
    extraReducers: builder => {
        builder.addMatcher(
            api.endpoints.getSettings.matchFulfilled,
            (state, {payload}) => {
                state.fields = payload;
            }
        )
    }
});

export const {

} = settingsSlice.actions;

export default settingsSlice.reducer;

export const selectSettingsFields = (state: any) => state.settings.fields;