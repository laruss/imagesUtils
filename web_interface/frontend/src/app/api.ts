import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/dist/query/react";

export const api = createApi({
    baseQuery: fetchBaseQuery({baseUrl: '/api'}),
    tagTypes: ['settings', 'images', 'imageData'],
    endpoints: (builder) => ({
        getSettings: builder.query({
            query: () => '/settings',
            providesTags: ['settings'],
        }),
        getImages: builder.query({
            query: () => '/images',
            providesTags: ['images'],
        }),
        getImageData: builder.query({
            query: (id: string) => `/images/${id}/data`,
            providesTags: ['imageData'],
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
    })
});