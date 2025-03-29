import React, {useState, useEffect} from "react";
import axios from "axios";
import Navbar from "./navbar";
import Dropdown from "./Dropdown";
import {useNavigate} from "react-router-dom";
import './Resources.css';

const API_URL = process.env.REACT_APP_API_URL;

const getRarityClass = (name) => {
    if (name.includes("Perfect")) return "mc-legendary";
    if (name.includes("Flawless")) return "mc-epic";
    if (name.includes("Fine")) return "mc-rare";
    if (name.includes("Flawed")) return "mc-uncommon";
    if (name.includes("Rough")) return "mc-common";
    return "";
}

const Resources = () => {
    const [resources, setResources] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const navigate = useNavigate();

    const fetchResources = () => {
        setIsLoading(true);
        axios.get(`${API_URL}/api/resources`)
            .then((response) => {
                const sortedResources = response.data.sort((a,b) => a.name.localeCompare(b.name));
                setResources(sortedResources);
                setIsLoading(false);
            })
            .catch((err) => {
                console.log(err);
                setIsLoading(false);
            });
    };

    useEffect(() => {
        fetchResources();
    }, []);
    
    // fetching every 1.5 seconds
    useEffect(() => {
        const intervalid = setInterval(() => {
            fetchResources();
        }, 1500);
        return () => clearInterval(intervalid);
    }, []);

    const transfer = () => {
        navigate('/modify', { state: { items: resources } });
    }

    //animation for refresh button
    const [isRefreshing, setIsRefreshing] = useState(false);
    
    const handleRefresh = () => {
        setIsRefreshing(true);
        fetchResources();
        setTimeout(() => setIsRefreshing(false), 1000);
    }

    const final_resources = resources.filter(resource => resource.amount > 0);
    
    return (
        <div className="mc-container resources-container">
            <Navbar transfer={transfer}/>
            <h3 className="resources-header">Available Resources</h3>
            <button 
                className={`mc-button refresh-button ${isRefreshing ? 'crafting-animation' : ''}`} 
                onClick={handleRefresh}
                disabled={isLoading}
            >
                {isRefreshing ? 'Refreshing...' : 'Refresh'}
            </button>
            
            <Dropdown items={resources} />
            
            <div className="resources-list">
                {final_resources.map((resource) => (
                    <div className="mc-item" key={resource.id}>
                        <span className={`mc-item-name ${getRarityClass(resource.name)}`}>{resource.name}</span>
                        <span className="mc-item-count">{resource.amount}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Resources;