import {SerializedError} from "@reduxjs/toolkit";
import {FetchBaseQueryError} from "@reduxjs/toolkit/query";
import {useEffect} from "react";
import {showNotification} from "./dispatchers";

interface ErrorInterface {
    error: FetchBaseQueryError | SerializedError | undefined;
    message: string;
}

const useErrorHandler = ({error, message}: ErrorInterface) => {
    useEffect(() => {
        if (error) {
            console.warn(error);
            showNotification(message, 'error');
        }
    }, [error, message]);
};

export default useErrorHandler;