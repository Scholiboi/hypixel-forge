import React, { useState, useEffect } from 'react';
import './Dropdown.css';
import {useLocation} from 'react-router-dom';

const Dropdown = ({items , func = null}) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [filteredItems, setFilteredItems] = useState([]);
    const [amount, setAmount] = useState(1);
    const [isOpen, setIsOpen] = useState(false);

    const location = useLocation();
    
    const handleChange = (event) => {
        const value = event.target.value;
        setSearchTerm(value);
        
        if (value === '') {
            setFilteredItems([]);
            setIsOpen(false);
        } else {
            const filtered = items.filter(item => 
                item.name.toLowerCase().includes(value.toLowerCase())
            );
            setFilteredItems(filtered);
            setIsOpen(filtered.length > 0);
        }
    };

    const handleClickElement = (name) => {
        if (func !== null) {
            func(name, amount);
            setSearchTerm('');
            setFilteredItems([]);
            setIsOpen(false);
        }
    }
    
    const handleAmountChange = (event) => {
        const value = parseInt(event.target.value) || 1;
        setAmount(Math.max(1, value));
    }

    useEffect(() => {
        const handleClickOutside = () => {
            setIsOpen(false);
        };
        
        document.addEventListener('click', handleClickOutside);
        return () => {
            document.removeEventListener('click', handleClickOutside);
        };
    }, []);

    const renderDropdown = () => {
        switch(location.pathname) {
            case '/':
                return (
                    <div className="mc-container dropdown-container">
                        <div className="input-group">
                            <input
                                className="search-input"
                                type="text"
                                value={searchTerm}
                                onChange={handleChange}
                                placeholder="Search all resources..."
                                onClick={(e) => e.stopPropagation()}
                            />
                        </div>
                        {isOpen && filteredItems.length > 0 && (
                            <ul className="dropdown-list">
                                {filteredItems.map((item, index) => (
                                    <li 
                                        onClick={() => handleClickElement(item.name)} 
                                        className="dropdown-item" 
                                        key={index}
                                    >
                                        <span className="item-name">
                                            {item.name}
                                        </span>
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
                    <div className="mc-container dropdown-container">
                        <div className="input-group">
                            <input
                                className="search-input"
                                type="text"
                                value={searchTerm}
                                onChange={handleChange}
                                placeholder="Search all resources..."
                                onClick={(e) => e.stopPropagation()}
                            />
                            <input 
                                className="amount-input"
                                type="number"
                                value={amount}
                                onChange={handleAmountChange}
                                min="1"
                                placeholder="Qty"
                                onClick={(e) => e.stopPropagation()}
                            />
                        </div>
                        {isOpen && filteredItems.length > 0 && (
                            <ul className="dropdown-list">
                                {filteredItems.map((item, index) => (
                                    <li 
                                        onClick={() => handleClickElement(item.name)} 
                                        className="dropdown-item" 
                                        key={index}
                                    >
                                        <span className="item-name">
                                            {item.name}
                                        </span>
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