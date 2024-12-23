import React from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import './App.css';
import Resources from './components/Resources';
import NotFound from './components/NotFound';
import ResourceModify from './components/ResourceModify';
import Sandbox from './components/Sandbox';
import Forging from './components/Forging';
function App() {
    return (
        <Router>
            <div>
                <Routes>
                    <Route path="/" element={<Resources/>} />
                    <Route path="/modify" element={<ResourceModify/>} />
                    <Route path="/sandbox" element={<Sandbox/>} />
                    <Route path="/sandbox/forge" element={<Forging/>} />
                    <Route path="*" element={<NotFound/>} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;