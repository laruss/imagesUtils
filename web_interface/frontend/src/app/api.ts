import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/dist/query/react";

export const api = createApi({
    baseQuery: fetchBaseQuery({baseUrl: '/api'}),
    tagTypes: ['settings', 'settingsSchema', 'images', 'imageData', 'imageDataSchema'],
    endpoints: (builder) => ({
        getSettings: builder.query({
            query: () => '/settings',
            providesTags: ['settings'],
        }),
        updateSettings: builder.mutation({
            query: ({fields}) => ({
                url: '/settings',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: fields,
            }),
            invalidatesTags: ['settings'],
        }),
        resetSettings: builder.mutation({
            query: () => ({
                url: '/settings',
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            }),
            invalidatesTags: ['settings'],
        }),
        getSettingsSchema: builder.query({
            query: () => '/settings/schema',
            providesTags: ['settingsSchema'],
        }),
        getImages: builder.query({
            query: () => '/images',
            providesTags: ['images'],
        }),
        getImageData: builder.query({
            query: (id: string) => `/images/${id}/data`,
            providesTags: ['imageData'],
        }),
        updateImageData: builder.mutation({
            query: ({id, data}) => ({
                url: `/images/${id}/data`,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: data,
            }),
            invalidatesTags: ['imageData'],
        }),
        getImageDataSchema: builder.query({
            query: () => '/images/data/schema',
            providesTags: ['imageDataSchema'],
        }),
        updateImageDescription: builder.mutation({
            query: ({id}) => ({
                url: `/images/${id}/description`,
                method: 'PUT',
            }),
            invalidatesTags: ['imageData'],
        }),
        updateByGPT: builder.mutation({
            query: ({id}) => ({
                url: `/images/${id}/gpt`,
                method: 'PUT',
            }),
            invalidatesTags: ['imageData'],
        }),
        setJSONFromGPT: builder.mutation({
            query: ({id}) => ({
                url: `/images/${id}/gpt/json`,
                method: 'PUT',
            }),
            invalidatesTags: ['imageData'],
        }),
        convertToWebP: builder.mutation({
            query: ({id}) => ({
                url: `/images/${id}/webp`,
                method: 'PUT',
            }),
            invalidatesTags: ['imageData'],
        }),
        optimizeImage: builder.mutation({
            query: ({id}) => ({
                url: `/images/${id}/optimize`,
                method: 'PUT',
            }),
            invalidatesTags: ['imageData'],
        }),
        deleteImage: builder.mutation({
            query: ({id}) => ({
                url: `/images/${id}`,
                method: 'DELETE',
            }),
            invalidatesTags: ['imageData', 'images'],
        }),
        // all images
        downloadImages: builder.mutation({
            query: () => ({
                url: `/download`,
                method: 'POST',
            }),
            invalidatesTags: ['images'],
        }),
        generateDescriptions: builder.mutation({
            query: () => ({
                url: `/description`,
                method: 'POST',
            }),
            invalidatesTags: ['images', 'imageData'],
        }),
        optimizeImages: builder.mutation({
            query: () => ({
                url: `/optimize`,
                method: 'POST',
            }),
            invalidatesTags: ['images'],
        }),
        useCloud: builder.mutation({
            query: () => ({
                url: `/cloud`,
                method: 'POST',
            }),
            invalidatesTags: ['images'],
        }),
    })
});