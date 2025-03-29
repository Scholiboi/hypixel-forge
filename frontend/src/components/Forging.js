import React, {useState, useEffect} from "react";
import Dropdown from "./Dropdown";
import axios from "axios";
import {useNavigate} from "react-router-dom";
import './Forging.css';
import Navbar from "./navbar";

const API_URL = process.env.REACT_APP_API_URL;

const TreeNode = ({node}) => {
    const [expanded, setExpanded] = useState(false);
    const [hover, setHover] = useState(false);

    if (!node) return null;
    const hasChildren = node.ingredients && node.ingredients.length > 0;
    
    const getRarityClass = (name) => {
        if (name.includes("Perfect")) return "mc-legendary";
        if (name.includes("Flawless")) return "mc-epic";
        if (name.includes("Fine")) return "mc-rare";
        if (name.includes("Flawed")) return "mc-uncommon";
        if (name.includes("Rough")) return "mc-common";
        return "";
    }
    
    return (
        <div className="tree-node">
            <div 
                className={`tree-content ${hover ? 'hover-effect' : ''}`}
                onClick={() => setExpanded(!expanded)}
                onMouseEnter={() => setHover(true)}
                onMouseLeave={() => setHover(false)}
            >
                <span className="tree-text">You need</span>
                <span className="tree-amount">{node.amount}×</span>
                <span className={`tree-name ${getRarityClass(node.name)}`}>{node.name}</span>
                {hasChildren && (
                    <span className="tree-toggle">{expanded ? "▼" : "▶"}</span>
                )}
            </div>
            {expanded && hasChildren && (
                <div className="tree-children">
                    {node.ingredients.map((childNode, index) => (
                        <TreeNode key={index} node={childNode} />
                    ))}
                </div>
            )}
        </div>
    );
};

const Forging = () => {
    const [recipes, setRecipes] = useState([]);
    const [recipe, setRecipe] = useState(null);
    const [craftable, setCraftable] = useState(false);
    const [amount, setAmount] = useState(1);
    const [isCrafting, setIsCrafting] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get(`${API_URL}/api/sandbox/get-recipes-names`)
            .then((response) => {
                setRecipes(response.data);
            })
            .catch((err) => {
                console.log(err);
            });
    }, []);

    useEffect(() => {
        const refreshInterval = setInterval(() => {
            refreshRecipe();
        }, 1500);
        return () => clearInterval(refreshInterval);
    }, [recipe]);

    const recipe_names = recipes.map((recipe) => ({ name: recipe }));

    const getRecipe = (name, amount) => {
        setCraftable(false);
        setAmount(amount);
        axios.get(`${API_URL}/api/sandbox/get-remaining-ingredients/${name}/${amount}`)
            .then((response) => {
                setRecipe(response.data);
                if(response.data.full_recipe.amount === 0){
                    setCraftable(true);
                }
            })
            .catch((err) => {
                console.log(err);
            })
    };

    const craft = () => {
        setIsCrafting(true);
        axios.post(`${API_URL}/api/sandbox/craft`, {name: recipe.full_recipe.name, amount: amount})
            .then((response) => {
                console.log(response.data);
                setTimeout(() => {
                    setCraftable(false);
                    setRecipe(null);
                    setAmount(1);
                    setIsCrafting(false);
                }, 1500);
            })
            .catch((err) => {
                console.log(err);
                setIsCrafting(false);
            });
    }

    const viewMode = () => {
        navigate('/sandbox');
    };

    const refreshRecipe = () => {
        if (recipe) {
            getRecipe(recipe.full_recipe.name, amount);
        }
    };

    return (
        <div className="mc-container forging-container">
            <Navbar />
            <div className="forging-header">
                <h1>Dwarven Forge Viewer</h1>
                <p>Explore all possible forging recipes</p>
            </div>
            <div className="mode-selector">
                <button className="mc-button" onClick={viewMode}>Switch to View Mode</button>
            </div>
            <div className="recipe-section mc-container">
                {<Dropdown items={recipe_names} func={getRecipe}/>}
                {recipe && <div className="recipe-tree">{<TreeNode node={recipe.full_recipe}/>}</div>}
                {recipe && <ul className="recipe-messages">
                    {recipe.messages.map((message, index) => (
                        <li key={index} className="message-item">{message}</li>
                    ))}
                </ul>}
                {recipe && craftable && (
                    <button 
                        className={`mc-button craft-button ${isCrafting ? 'crafting-animation' : ''}`} 
                        onClick={craft}
                        disabled={isCrafting}
                    >
                        {isCrafting ? 'Crafting...' : 'Craft'}
                    </button>
                )}
                {recipe && (
                    <button className="mc-button refresh-button" onClick={refreshRecipe}>
                        ↻ Refresh
                    </button>
                )}
            </div>
        </div>
    );
};

export default Forging;