import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
    return (
        <footer className="bg-white dark:bg-surface-dark border-t border-gray-200 dark:border-white/10 mt-auto py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                    <div className="text-center md:text-left">
                        <h3 className="text-sm font-bold text-gray-900 dark:text-white">Powered by Trusted Sources</h3>
                        <p className="text-xs text-text-muted mt-1">Data synchronized with government databases daily.</p>
                    </div>
                    <div className="flex flex-wrap justify-center gap-6 grayscale opacity-70 hover:grayscale-0 hover:opacity-100 transition-all duration-300">

                        <div className="flex items-center gap-2">
                            <div className="w-6 h-6 bg-gray-300 dark:bg-gray-600 rounded-full overflow-hidden">
                                <div className="w-full h-full bg-blue-500 rounded-full"></div>
                            </div>
                            <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">IMD Weather</span>
                        </div>

                        <div className="flex items-center gap-2">
                            <div className="w-6 h-6 bg-gray-300 dark:bg-gray-600 rounded-full overflow-hidden">
                                <div className="w-full h-full bg-green-600 rounded-full"></div>
                            </div>
                            <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">Agmarknet</span>
                        </div>

                        <div className="flex items-center gap-2">
                            <div className="w-6 h-6 bg-gray-300 dark:bg-gray-600 rounded-full overflow-hidden">
                                <div className="w-full h-full bg-orange-500 rounded-full"></div>
                            </div>
                            <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">Maharashtra Gov</span>
                        </div>
                    </div>
                    <div className="text-xs text-text-muted">
                        © 2026 AI Krishi Sahayak. All rights reserved.
                    </div>
                </div>
                <div className="mt-4 text-center">
                    <Link to="/admin" className="text-xs text-gray-400 hover:text-primary transition-colors">Admin Login</Link>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
