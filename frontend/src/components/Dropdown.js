import React, { useState } from 'react';
import './Dropdown.css';
import {useLocation} from 'react-router-dom';

const Dropdown = ({ items , func = null}) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [filteredItems, setFilteredItems] = useState(items);
    const [amount, setAmount] = useState(1);

    const location = useLocation();
    const handleChange = (event) => {
        const value = event.target.value;
        // console.log(`Value in input: ${value}`);
        setSearchTerm(value);
        // console.log(`Value in React: ${searchTerm}`);
        if (value === '') {
            setFilteredItems([]);
        }else{
            setFilteredItems(items.filter(item => item.name.toLowerCase().includes(value.toLowerCase())));
        }
    };

    const handleClickElement = (event) => {
        const name = event.target.innerText;
        if (func !== null) {
            func(name, amount);
            setSearchTerm('');
            setFilteredItems([]);
        }else{
            func = () => {};
        }
    }
    
    const handleAmountChange = (event) => {
        const value = event.target.value;
        setAmount(value);
    }

    const renderDropdown = () => {
        switch(location.pathname) {
            case '/':
                return (
                    <div className="dropdown-container">
                        <div className="input-group">
                            <input
                                className="search-input"
                                type="text"
                                value={searchTerm}
                                onChange={handleChange}
                                placeholder="Search all resources..."
                            />
                        </div>
                        {filteredItems.length > 0 && (
                            <ul className="dropdown-list">
                                {filteredItems.map((item, index) => (
                                    <li onClick={handleClickElement} 
                                        className="dropdown-item" 
                                        key={index}>
                                        <span className="item-name">{item.name}</span>
                                        <span className="item-count">{item.amount}</span>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                );
            case '/sandbox':
            case '/sandbox/forge':
                return (
                    <div className="dropdown-container">
                        <div className="input-group">
                            <input
                                className="search-input"
                                type="text"
                                value={searchTerm}
                                onChange={handleChange}
                                placeholder="Search all resources..."
                            />
                            <input 
                                className="amount-input"
                                type="number"
                                value={amount}
                                onChange={handleAmountChange}
                                min="1"
                                placeholder="Qty"
                            />
                        </div>
                        {filteredItems.length > 0 && (
                            <ul className="dropdown-list">
                                {filteredItems.map((item, index) => (
                                    <li onClick={handleClickElement} 
                                        className="dropdown-item" 
                                        key={index}>
                                        <span className="item-name">{item.name}</span>
                                        <span className="item-count">{item.amount}</span>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                );
            default:
                return null;
        }
    }

    return (
        renderDropdown()
    );
};

export default Dropdown;