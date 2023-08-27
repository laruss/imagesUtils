import {FieldProps} from "@rjsf/utils";

export const getMultiSelectItems = (props: FieldProps) => {
    const rootSchema = props.registry.rootSchema;
    let schemaItems = props.schema.items;
    const schema = '$ref' in (schemaItems as {[key:string]: any}) ? (schemaItems as {[key:string]: any})['$ref'] : undefined;
    if (schema === undefined) return schemaItems;

    const keys = schema.split('/');
    keys.shift();
    let schemaObj = rootSchema;
    keys.forEach((key: string) => {schemaObj = schemaObj[key];});

    return schemaObj.enum ? schemaObj.enum : [];
};