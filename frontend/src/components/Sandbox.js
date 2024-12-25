import React, {useEffect, useState} from "react";
import axios from "axios";
import {useNavigate} from "react-router-dom";
import Dropdown from "./Dropdown";
import './Sandbox.css';
import Navbar from "./navbar";

const TreeNode = ({ node }) => {
    const [expanded, setExpanded] = useState(false);

    if (!node) return null;
    const hasChildren = node.ingredients && node.ingredients.length > 0;

    return (
        <div className="tree-node">
            <p onClick={() => setExpanded(!expanded)}>
                <span className="tree-amount">{node.amount}×</span>
                <span className="tree-name">{node.name}</span>
                {hasChildren && (
                    <span className="tree-toggle">
                        {expanded ? "▼" : "▶"}
                    </span>
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

const Sandbox = () => {
    const [recipesNames, setRecipesNames] = useState([]);
    const [recipe, setRecipe] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get("http://localhost:5000/sandbox/get-recipes-names")
            .then((response) => {
                setRecipesNames(response.data);
            })
            .catch((err) => {
                console.log(err);
            });
    }, []);

    const recipe_names = recipesNames.map((recipe) => ({ name: recipe }));

    const getRecipe = (name, amount) => {
        axios.get(`http://localhost:5000/sandbox/get-recipe/${name}/${amount}`)
            .then((response) => {
                setRecipe(response.data);
            })
            .catch((err) => {
                console.log(err);
            });
    };

    const forgeMode = () => {
        navigate('/sandbox/forge');
    }

    return (
        <div className="sandbox-container">
            <Navbar />
            <div className="sandbox-header">
                <h1>Recipe Viewer</h1>
                <p>Search and explore crafting recipes</p>
            </div>
            <div className="mode-select">
                <p onClick={forgeMode}>Switch to Forge Mode</p>
            </div>
            <Dropdown items={recipe_names} func={getRecipe} />

            {recipe && recipe.simple_recipe && recipe.full_recipe && (
                <div className="recipe-details">
                    <h2>{recipe.name} Recipe</h2>

                    <h3>Required Materials</h3>
                    <ul className="simple-recipe-list">
                        {Object.entries(recipe.simple_recipe).map(([item, qty]) => (
                            <li key={item} className="simple-recipe-item">
                                <span className="item-name">{item}</span>
                                <span className="tree-amount">{qty}×</span>
                            </li>
                        ))}
                    </ul>

                    <h3>Crafting Tree</h3>
                    <div className="recipe-tree">
                        <TreeNode node={recipe.full_recipe} />
                    </div>
                </div>
            )}
        </div>
    );
};

export default Sandbox;
