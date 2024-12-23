import React,{useState, useEffect} from "react";
import axios from "axios";
import Navbar from "./navbar";
import Dropdown from "./Dropdown";
import {useNavigate} from "react-router-dom";
import './Resources.css';

const Resources = () => {
    const [resources, setResources] = useState([]);
    // const [searchedResources, setSearchedResources] = useState(null);
    const navigate = useNavigate();
    useEffect(() => {
        axios.get("http://localhost:5000/resources")
            .then((response) => {
                const sortedResources = response.data.sort((a,b) => a.name.localeCompare(b.name));
                setResources(sortedResources);
            })
            .catch((err) => {
                console.log(err);
            });
    }, []);

    // const searchResource = () => {
    //     const name = document.getElementById('name').value;
    //     axios.get(`http://localhost:5000/resources/${name}`)
    //         .then((response) => {
    //             setSearchedResources(response.data);
    //         })
    //         .catch((err) => {
    //             console.log(err);
    //         });
    // }

    const transfer = () => {
        navigate('/modify', { state: { items: resources } });
    }

    // const resource_names = resources.map(resource => resource.name);
    const final_resources = resources.filter(resource => resource.amount > 0);
    return (
        <div className="resources-container">
            <Navbar transfer={transfer}/>
            <h3 className="resources-header">Available Resources</h3>
            <div className="resources-list">
                {final_resources.map((resource) => (
                    <div className="resource-item" key={resource.id}>
                        <span className="resource-name">{resource.name}</span>
                        <span className="resource-amount">{resource.amount}</span>
                    </div>
                ))}
            </div>
            <Dropdown items={resources} />
        </div>
    );
};

export default Resources;