import React, { useState } from 'react';
import './Dropdown.css';

const Dropdown = ({ items , func = null}) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [filteredItems, setFilteredItems] = useState(items);

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
            func(name);
            setSearchTerm('');
            setFilteredItems([]);
        }else{
            func = () => {};
        }
    }

    return (
        <div id="Dropdown">
            <input
                className="search-input"
                type="text"
                value={searchTerm}
                onChange={handleChange}
                placeholder="Search all resources..."
            />
            <ul className="dropdown-ul">
                {filteredItems.map((item, index) => (
                    <li onClick={handleClickElement} className="dropdown-li" key={index}>
                        <span className="name">{item.name}</span>
                        <span className="count">{item.amount}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Dropdown;