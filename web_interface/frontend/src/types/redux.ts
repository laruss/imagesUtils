export interface AppState {
    isLoaderShown: boolean;
    notification: {
        isOpen: boolean;
        text: string;
        variant: 'success' | 'error' | 'warning' | 'info';
    }
}

export interface SettingsState {
    fields: {[key: string]: any};
}

export interface ImagesState {
    images: string[],
    currentImage: string | null,
    currentImageData: {[key: string]: any}
}