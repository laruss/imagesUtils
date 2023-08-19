import {SettingsState} from "../../types/redux";
import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {api} from "../api";
import {areObjectsEqual} from "../../helpers/methods";

const initialState: SettingsState = {
    fields: {},
    newFields: {},
    fieldsAreChanged: false,
    fieldsAreValid: true, // TODO
    fieldsSchema: {},
};

export const settingsSlice = createSlice({
    name: 'settings',
    initialState,
    reducers: {
        changeFields: (state, action: PayloadAction<SettingsState['newFields']>) => {
            state.fieldsAreChanged = !areObjectsEqual(state.fields, action.payload);
            state.newFields = action.payload;
        },
    },
    extraReducers: builder => {
        builder.addMatcher(
            api.endpoints.getSettings.matchFulfilled,
            (state, {payload}) => {
                state.fields = payload;
                state.newFields = payload;
                state.fieldsAreChanged = false;
            }
        ).addMatcher(
            api.endpoints.getSettingsSchema.matchFulfilled,
            (state, {payload}) => {
                state.fieldsSchema = payload;
            }
        )
    }
});

export const {
    changeFields
} = settingsSlice.actions;

export default settingsSlice.reducer;

export const selectSettingsFields = (state: any) => state.settings.fields;

export const selectSettingsNewFields = (state: any) => state.settings.newFields;

export const selectSettingsFieldsAreChanged = (state: any) => state.settings.fieldsAreChanged;

export const selectSettingsFieldsSchema = (state: any) => state.settings.fieldsSchema;