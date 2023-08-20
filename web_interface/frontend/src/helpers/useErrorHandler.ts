import {SerializedError} from "@reduxjs/toolkit";
import {FetchBaseQueryError} from "@reduxjs/toolkit/query";
import {useEffect} from "react";
import {showNotification} from "./dispatchers";

interface ErrorInterface {
    error: FetchBaseQueryError | SerializedError | undefined;
    message: string;
}

const useErrorHandler = ({error, message}: ErrorInterface) => {
    const errMsg = (error && ('error' in error ? error.error : JSON.stringify((error as FetchBaseQueryError).data))) || message;

    useEffect(() => {
        if (error) {
            console.warn(error);
            showNotification(errMsg, 'error');
        }
    }, [error, message]);
};

export default useErrorHandler;