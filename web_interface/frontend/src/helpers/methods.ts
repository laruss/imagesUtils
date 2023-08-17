export const isObjectEmpty = (obj: {[key:string]: any}) => {
    return Object.keys(obj).length === 0;
}

export type ValueType = "number" | "boolean" | "object" | "string" | "null" | "array" | "unknown";

export function determineType(value: any): ValueType {
    if (value === null) {
        return "null";
    }

    switch (typeof value) {
        case "number":
            return "number";
        case "boolean":
            return "boolean";
        case "string":
            return "string";
        case "object":
            if (Array.isArray(value)) {
                return "array";
            } else {
                return "object";
            }
        default:
            return "unknown";
    }
}