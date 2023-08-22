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
        cartoonizeImage: builder.mutation({
            query: ({id}) => ({
                url: `/images/${id}/cartoonize`,
                method: 'PUT',
            }),
            invalidatesTags: ['imageData'],
        }),
        // all images
        downloadImages: builder.mutation({
            query: () => ({
                url: `/download`,
                method: 'POST',
            }),
            invalidatesTags: ['images'],
        }),
        describeImagesDescribe: builder.mutation({
            query: () => ({
                url: `/description/describe`,
                method: 'POST',
            }),
            invalidatesTags: ['imageData'],
        }),
        describeImagesDeleteNSFW: builder.mutation({
            query: () => ({
                url: `/description/delete/nsfw`,
                method: 'POST',
            }),
            invalidatesTags: ['images'],
        }),
        describeImagesGpt: builder.mutation({
            query: () => ({
                url: `/description/gpt`,
                method: 'POST',
            }),
            invalidatesTags: ['imageData'],
        }),
        describeImagesGptJson: builder.mutation({
            query: () => ({
                url: `/description/gpt2json`,
                method: 'POST',
            }),
            invalidatesTags: ['imageData'],
        }),
        optimizeImagesWebP: builder.mutation({
            query: () => ({
                url: `/optimize/webp`,
                method: 'POST',
            }),
        }),
        optimizeImagesMinimize: builder.mutation({
            query: () => ({
                url: `/optimize/minimize`,
                method: 'POST',
            }),
            invalidatesTags: ['images'],
        }),
        optimizeImagesDuplicates: builder.mutation({
            query: () => ({
                url: `/optimize/duplicates`,
                method: 'DELETE',
            }),
            invalidatesTags: ['images'],
        }),
        optimizeImagesCartoonize: builder.mutation({
            query: () => ({
                url: `/optimize/cartoonize`,
                method: 'POST',
            }),
            invalidatesTags: ['images', 'imageData'],
        }),
        cloudUpload: builder.mutation({
            query: () => ({
                url: `/cloud/upload`,
                method: 'POST',
            }),
            invalidatesTags: ['images'],
        }),
        cloudDownload: builder.mutation({
            query: () => ({
                url: `/cloud/download`,
                method: 'POST',
            }),
            invalidatesTags: ['images'],
        }),
    })
});