import Images from "../pages/images/Images";
import Settings from "../pages/settings/Settings";

interface DataTabProps {
    currentModel: string | null;
}

const DataTab = ({currentModel}: DataTabProps) => {
    return (
        <div>
            {currentModel === 'images' ? <Images/> : <Settings/>}
        </div>
    )
};

export default DataTab;