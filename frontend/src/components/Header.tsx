import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, Home, Lightbulb } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2 text-xl font-bold text-gray-900">
            <Activity className="h-8 w-8 text-blue-600" />
            <span>Exercise Form Analyzer</span>
          </Link>
          
          <nav className="flex items-center space-x-6">
            <Link 
              to="/" 
              className="flex items-center space-x-1 text-gray-600 hover:text-blue-600 transition-colors"
            >
              <Home className="h-5 w-5" />
              <span>Home</span>
            </Link>
            <Link 
              to="/analysis" 
              className="flex items-center space-x-1 text-gray-600 hover:text-blue-600 transition-colors"
            >
              <Activity className="h-5 w-5" />
              <span>Analyze</span>
            </Link>
            <Link 
              to="/tips/pull_up" 
              className="flex items-center space-x-1 text-gray-600 hover:text-blue-600 transition-colors"
            >
              <Lightbulb className="h-5 w-5" />
              <span>Tips</span>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 