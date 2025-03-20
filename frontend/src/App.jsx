import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { useState } from "react";
import Home from "./pages/Home";
import Signup from "./pages/Signup";
import MyTeam from "./pages/MyTeam";
import LeagueHome from "./pages/League/LeagueHome";
  import LeagueSettings from "./pages/League/LeagueSettings";
  import LeagueMembers from "./pages/League/LeagueMembers";
  import LeagueRosters from "./pages/League/LeagueRosters";
  import LeagueSchedule from "./pages/League/LeagueSchedule";
  
import Players from "./pages/Players";
import Standings from "./pages/Standings";
import About from "./pages/About";
import Contact from "./pages/Contact";
import "./App.css"; // Ensure styles are applied

function App() {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  // Function to close dropdown when clicking a link
  const closeDropdown = () => {
    setIsDropdownOpen(false);
  };

  return (
    <Router>
      <div>
        {/* Navigation */}
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/my-team">My Team</Link></li>

            {/* League Dropdown */}
            <li 
              className="dropdown"
              onMouseEnter={() => setIsDropdownOpen(true)}
              onMouseLeave={() => setIsDropdownOpen(false)}
            >
              <Link to="/league/home" onClick={closeDropdown} className="dropbtn">League ▾</Link>
              {isDropdownOpen && (
                <ul className="dropdown-content">
                  <li><Link to="/league/home" onClick={closeDropdown}>League Home</Link></li>
                  <li><Link to="/league/settings" onClick={closeDropdown}>Settings</Link></li>
                  <li><Link to="/league/members" onClick={closeDropdown}>Members</Link></li>
                  <li><Link to="/league/rosters" onClick={closeDropdown}>Rosters</Link></li>
                  <li><Link to="/league/schedule" onClick={closeDropdown}>Schedule</Link></li>
                </ul>
              )}
            </li>

            <li><Link to="/players">Players</Link></li>
            <li><Link to="/standings">Standings</Link></li>
            <li><Link to="/about">About</Link></li>
            <li><Link to="/contact">Contact</Link></li>
          </ul>
        </nav>

        {/* Page-Specific Content */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/my-team" element={<MyTeam />} />
            <Route path="/league/home" element={<LeagueHome />} />
            <Route path="/league/settings" element={<LeagueSettings />} />
            <Route path="/league/members" element={<LeagueMembers />} />
            <Route path="/league/rosters" element={<LeagueRosters />} />
            <Route path="/league/schedule" element={<LeagueSchedule />} />
          <Route path="/players" element={<Players />} />
          <Route path="/standings" element={<Standings />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
