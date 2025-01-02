import React, {useState} from "react";
import axios from "axios";
import Navbar from "./navbar";
import {useNavigate, useLocation} from "react-router-dom";
import './ResourceModify.css';

const ResourceModify = () => {
    const [searchTerm, setSearchTerm] = useState("");
    const [searchedResources, setSearchedResources] = useState([]);
    const [newUpdatedResources, setNewUpdatedResources] = useState([]);

    const navigate = useNavigate();
    const location = useLocation(); // react-router-dom hook to get the location object

    const items = location.state?.items || []; // if location.state is undefined, items will be an empty array

    const handleEvent = (event) => {
        const value = event.target.value;
        setSearchTerm(value);
        if (value === '') {
            setSearchedResources([]);
        }else{
            setSearchedResources(items.filter(item => item.name.toLowerCase().includes(value.toLowerCase())));
        }
    }

    // do not touch this function
    const updateNewUpdatedResources = (item) => {
        setNewUpdatedResources(prevState => {
            const existingItemIndex = prevState.findIndex(resource => resource.name === item.name);
            if (existingItemIndex !== -1) {
                const updatedResources = [...prevState];
                updatedResources[existingItemIndex] = item;
                return updatedResources;
            } else {
                return [...prevState, item];
            }
        });
    };

    const incrementAmount = (index, item) => {
        const updatedResources = [...searchedResources];
        updatedResources[index].amount += 1;
        setSearchedResources(updatedResources);
        updateNewUpdatedResources(updatedResources[index]);
    }

    const decrementAmount = (index, item) => {
        const updatedResources = [...searchedResources];
        if (updatedResources[index].amount > 0) {
            updatedResources[index].amount -= 1;
            setSearchedResources(updatedResources);
            updateNewUpdatedResources(updatedResources[index]);
        }
    }

    const SubmitModifications = async () => {
        try {
            const response = await axios.post("http://localhost:5000/modify-resources", {newUpdatedResources});
            navigate('/');
        }catch (err) {
            console.log(err);
            alert("Error in modifying resources");
        }
    }

    return (
        <div id="resource-modify-container">
            <Navbar />
            <h1 id="resource-modify-header">Modify Resources</h1>
            <div id="resource-modify-layout">
                <div id="resource-search-section">
                    <input
                        id="resource-search-input"
                        type="text"
                        value={searchTerm}
                        onChange={handleEvent}
                        placeholder="Search resources..."
                    />
                    <div id="resource-items-list">
                        {searchedResources.map((item, index) => (
                            <div className="resource-modify-item" key={index}>
                                <span className="resource-modify-name">{item.name}</span>
                                <div className="resource-amount-controls">
                                    <button onClick={() => decrementAmount(index, item)}>-</button>
                                    <input 
                                        type='number'
                                        value={item.amount}
                                        onChange={(e) => {
                                            const updatedResources = [...searchedResources];
                                            updatedResources[index].amount = parseInt(e.target.value);
                                            setSearchedResources(updatedResources);
                                            updateNewUpdatedResources(updatedResources[index]);
                                        }}
                                    />
                                    <button onClick={() => incrementAmount(index, item)}>+</button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
                <div id="resource-modifications-section">
                    <h2 id="modifications-title">Modified Resources</h2>
                    <div id="modified-items-list">
                        {newUpdatedResources.map((item, index) => (
                            <div className="modified-resource-item" key={index}>
                                <span className="modified-resource-name">{item.name}</span>
                                <span className="modified-resource-amount">{item.amount}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
            <button id="resource-submit-button" onClick={SubmitModifications}>
                Save Changes
            </button>
        </div>
    );
}

export default ResourceModify;