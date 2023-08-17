import {setLoaderShown, setNotification} from "../app/slices/appSlice";
import {store} from "../app/store";

export const showNotification = (text: string, variant: 'success' | 'error' | 'warning' | 'info' = 'info') => {
    store.dispatch(setNotification({
        isOpen: true,
        text,
        variant
    }));
};

export const showLoader = (state: boolean) => {
    store.dispatch(setLoaderShown(state));
};