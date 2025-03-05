import React, {useState, useEffect} from "react";
import Dropdown from "./Dropdown";
import axios from "axios";
import {useNavigate} from "react-router-dom";
import './Forging.css';
import Navbar from "./navbar";

const API_URL = process.env.REACT_APP_API_URL;

const TreeNode = ({node}) => {
    const [expanded, setExpanded] = useState(false);

    if (!node) return null;
    const hasChildren = node.ingredients && node.ingredients.length > 0;
    return (
        <div className="tree-node">
            <p className="tree-content" onClick={() => setExpanded(!expanded)}>
                <span className="tree-text">You need</span>
                <span className="tree-amount">{node.amount}×</span>
                <span className="tree-name">{node.name}</span>
                {hasChildren && (
                    <span className="tree-toggle">{expanded ? "▼" : "▶"}</span>
                )}
            </p>
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
        // event.target.innerText = "";
    };

    const craft = () => {
        axios.post(`${API_URL}/api/sandbox/craft`, {name: recipe.full_recipe.name, amount: amount})
            .then((response) => {
                console.log(response.data);
            })
            .catch((err) => {
                console.log(err);
            });
        setCraftable(false);
        setRecipe(null);
        setAmount(1);
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
        <div className="forging-container">
            <Navbar />
            <div className="forging-header">
                <h1>Welcome to the Fireplace!</h1>
                <p>Here you can forge items</p>
            </div>
            <div className="mode-selector">
                <button onClick={viewMode}>Switch to View Mode</button>
            </div>
            <div className="recipe-section">
                {<Dropdown items={recipe_names} func={getRecipe}/>}
                {recipe && <div className="recipe-tree">{<TreeNode node={recipe.full_recipe}/>}</div>}
                {recipe && <ul className="recipe-messages">
                    {recipe.messages.map((message, index) => (
                        <li key={index} className="message-item">{message}</li>
                    ))}
                </ul>}
                {recipe && craftable && <button className="craft-button" onClick={craft}>Craft</button>}
                {recipe && <button className="refresh-button" onClick={refreshRecipe}>
                    ↻ Refresh
                </button>}
            </div>
        </div>
    );
};

export default Forging;