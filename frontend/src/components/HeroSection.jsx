import React, { useState } from 'react';

const HeroSection = ({ onSearch, selectedDistrict, setSelectedDistrict, districts }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query);
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto text-center mb-10">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-green-800 dark:text-green-300 mb-6 border border-primary/20">
                <span className="w-2 h-2 rounded-full bg-primary mr-2 animate-pulse"></span>
                Live AI Advisor • 24/7 Available
            </span>
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4 leading-tight">
                AI Krishi Sahayak for <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-primary">Maharashtra Farmers</span>
            </h2>
            <p className="text-xl md:text-2xl text-text-muted dark:text-gray-300 font-medium font-serif mb-8">
                तुमचे कृषी मित्र - आता मराठीत (Your Farming Friend - Now in Marathi)
            </p>

            {/* Search Module */}
            <form onSubmit={handleSubmit} className="bg-white dark:bg-surface-dark p-2 rounded-2xl shadow-xl border border-gray-100 dark:border-white/5 flex flex-col md:flex-row gap-2 max-w-3xl mx-auto relative z-10 transition-all hover:shadow-2xl hover:border-primary/30">
                {/* District Dropdown */}
                <div className="relative md:w-48 border-b md:border-b-0 md:border-r border-gray-200 dark:border-white/10">
                    <select
                        value={selectedDistrict}
                        onChange={(e) => setSelectedDistrict(e.target.value)}
                        className="w-full h-14 pl-10 pr-4 bg-transparent border-none focus:ring-0 text-gray-900 dark:text-white font-medium appearance-none cursor-pointer outline-none"
                    >
                        {districts.map((district) => (
                            <option key={district} value={district}>
                                {district}
                            </option>
                        ))}
                    </select>
                    <span className="material-icons absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">location_on</span>
                    <span className="material-icons absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none text-sm">expand_more</span>
                </div>

                {/* Main Input */}
                <div className="flex-grow relative">
                    <input
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        className="w-full h-14 pl-4 pr-12 bg-transparent border-none focus:ring-0 text-gray-900 dark:text-white placeholder-gray-400 text-lg outline-none"
                        placeholder="आपला प्रश्न विचारा... (Ask your question...)"
                        type="text"
                    />

                </div>

                {/* Submit Button */}
                <button type="submit" className="h-14 md:w-32 bg-primary hover:bg-primary-dark text-black font-bold rounded-xl transition-colors flex items-center justify-center gap-2 shadow-lg shadow-primary/20 cursor-pointer">
                    <span>Ask AI</span>
                    <span className="material-icons text-sm">send</span>
                </button>
            </form>

            {/* Quick Actions */}
            <div className="mt-6 flex flex-wrap justify-center gap-3">
                <button onClick={() => onSearch("Soybean drought help")} className="inline-flex items-center px-4 py-2 rounded-full bg-white dark:bg-surface-dark border border-gray-200 dark:border-white/10 text-sm font-medium hover:border-primary hover:text-primary transition-all shadow-sm cursor-pointer">
                    <span className="material-icons text-sm mr-2 text-yellow-600">wb_sunny</span>
                    Soybean drought help
                </button>
                <button onClick={() => onSearch("Cotton pest control")} className="inline-flex items-center px-4 py-2 rounded-full bg-white dark:bg-surface-dark border border-gray-200 dark:border-white/10 text-sm font-medium hover:border-primary hover:text-primary transition-all shadow-sm cursor-pointer">
                    <span className="material-icons text-sm mr-2 text-red-500">bug_report</span>
                    Cotton pest control
                </button>
                <button onClick={() => onSearch("Tur irrigation")} className="inline-flex items-center px-4 py-2 rounded-full bg-white dark:bg-surface-dark border border-gray-200 dark:border-white/10 text-sm font-medium hover:border-primary hover:text-primary transition-all shadow-sm cursor-pointer">
                    <span className="material-icons text-sm mr-2 text-blue-500">water_drop</span>
                    Tur irrigation
                </button>
            </div>
        </div>
    );
};

export default HeroSection;
