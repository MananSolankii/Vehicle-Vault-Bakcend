import React, { useState } from 'react';
import { FaSearch, FaUser } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import '../../assets/CSS/Navbar.css';

const UserNavbar = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (e) => {
    if (e.key === 'Enter' || e.type === 'click') {
      if (searchTerm.trim()) {
        navigate(`/search-car?query=${searchTerm}`);
      }
    }
  };

  return (
    <nav className="navbar">
      {/* Left Side */}
      <div className="left-side">
        <h1 className="website-name" onClick={() => navigate('/')}>Vehicle Vault</h1>
        <div className="nav-links">
          <a href="/new-cars" className="nav-link">New Cars</a>
          <a href="/reviews-news" className="nav-link">Reviews & News</a>
        </div>
      </div>
      {/* Right Side */}
      <div className="right-side">
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyDown={handleSearch}
          />
          <FaSearch className="search-icon" onClick={handleSearch} />
        </div>
        <div className="login-icon" onClick={() => navigate('/login')}>
          <FaUser />
        </div>
      </div>
    </nav>
  );
};

export default UserNavbar;
