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
    newFields: {[key: string]: any};
    fieldsAreChanged: boolean;
    fieldsAreValid: boolean;
    fieldsSchema: {[key: string]: any};
}

export interface ImagesState {
    images: string[],
    imageDataSchema: {[key: string]: any},
    currentImage: string | null,
    currentImageData: {[key: string]: any},
    changedImageData: {[key: string]: any},
    dataIsChanged: boolean,
    dataIsValid: boolean,
}