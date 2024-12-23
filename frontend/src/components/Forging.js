import React, {useState, useEffect} from "react";
import Dropdown from "./Dropdown";
import axios from "axios";
import {useNavigate} from "react-router-dom";

const TreeNode = ({node}) => {
  const [expanded, setExpanded] = useState(false);

  if (!node) return null;
  const hasChildren = node.ingredients && node.ingredients.length > 0;
  return (
    <div style={{ marginLeft: "20px" }}>
      <p onClick={() => setExpanded(!expanded)} style={{ cursor: "pointer" }}>
        You need <strong style={{ color: "#00C49A" }}>{node.amount}x </strong>
        {node.name} {hasChildren && (expanded ? "▼" : "▶")}
      </p>
      {expanded && hasChildren && (
        <div>
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
    const navigate = useNavigate();

    useEffect(() => {
        axios.get("http://localhost:5000/sandbox/get-recipes-names")
            .then((response) => {
                setRecipes(response.data);
            })
            .catch((err) => {
                console.log(err);
            });
    }, []);

    const recipe_names = recipes.map((recipe) => ({ name: recipe }));

    const getRecipe = (name) => {
        axios.get(`http://localhost:5000/sandbox/get-remaining-ingredients/${name}`)
            .then((response) => {
                setRecipe(response.data);
            })
            .catch((err) => {
                console.log(err);
        })
        // event.target.innerText = "";
    };


    const viewMode = () => {
        navigate('/sandbox');
    };

    return (
        <div>
            <h1>Welcome to the Fireplace!</h1>
            <p>Here you can forge items</p>
            <div className="mode-select">
                <p onClick={viewMode}>View Mode</p>
            </div>
            {<Dropdown items={recipe_names} func={getRecipe}/>}
            {recipe && <TreeNode node={recipe.full_recipe}/>}
            {recipe && <ul>
                {recipe.messages.map((message, index) => (
                    <li key={index}>{message}</li>
                ))}
            </ul>}
        </div>
    )
}

export default Forging;