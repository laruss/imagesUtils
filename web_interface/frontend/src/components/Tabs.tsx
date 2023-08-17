import {Box, Tab} from "@mui/material";
import TabContext from '@mui/lab/TabContext';
import {TabList, TabPanel} from "@mui/lab";
import DataTab from "./DataTab";
import {SyntheticEvent, useState} from "react";

export default function Tabs() {
    const models = {
        'settings': 'settings',
        'images': 'images',
    };
    const [currentModel, setCurrentModel] = useState('settings');

    const handleChange = (event: SyntheticEvent, newValue: string) => setCurrentModel(newValue);

    return (
        <Box
            sx={{ width: '100%', typography: 'body1', height: '100%'}}
        >
            <TabContext value={currentModel as string}>
                <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                    <TabList onChange={handleChange}>
                        {
                            models && Object.keys(models).map((model, index) => {
                                return <Tab key={index} label={model} value={model}/>
                            })
                        }
                    </TabList>
                </Box>
                {
                    currentModel && <TabPanel value={currentModel}>
                        { currentModel && <DataTab currentModel={currentModel}/> }
                    </TabPanel>
                }
            </TabContext>
        </Box>
    );
}