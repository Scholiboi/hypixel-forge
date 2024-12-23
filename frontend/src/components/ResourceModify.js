import React, {useState} from "react";
import axios from "axios";
import Navbar from "./navbar";
import {useNavigate, useLocation} from "react-router-dom";
import './ResourceModify.css';

const ResourceModify = () => {
    const [searchTerm, setSearchTerm] = useState("");
    const [searchedResources, setSearchedResources] = useState([]);
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
    const incrementAmount = (index) => {
        const updatedResources = [...searchedResources];
        updatedResources[index].amount += 1;
        setSearchedResources(updatedResources);
    }

    const decrementAmount = (index) => {
        const updatedResources = [...searchedResources];
        if (updatedResources[index].amount > 0) {
            updatedResources[index].amount -= 1;
            setSearchedResources(updatedResources);
        }
    }
    const SubmitModifications = async () => {
        try {
            const response = await axios.post("http://localhost:5000/modify-resources", {searchedResources});
            navigate('/');
        }catch (err) {
            console.log(err);
            alert("Error in modifying resources");
        }
    }

    return (
        <div className="modify-container">
            <Navbar />
            <h1 className="modify-header">Modify Resources</h1>
            <input
                className="search-input"
                type="text"
                value={searchTerm}
                onChange={handleEvent}
                placeholder="Search resources..."
            />
            <div className="resource-list">
                {searchedResources.map((item, index) => (
                    <div className="resource-item" key={index}>
                        <span className="resource-name">{item.name}</span>
                        <div className="amount-controls">
                            <button onClick={() => decrementAmount(index)}>-</button>
                            <input 
                                type='number'
                                value={item.amount}
                                onChange={(e) => {
                                    const updatedResources = [...searchedResources];
                                    updatedResources[index].amount = parseInt(e.target.value);
                                    setSearchedResources(updatedResources);
                                }}
                            />
                            <button onClick={() => incrementAmount(index)}>+</button>
                        </div>
                    </div>
                ))}
            </div>
            <button className="submit-button" onClick={SubmitModifications}>
                Save Changes
            </button>
        </div>
    );
}

export default ResourceModify;