import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

const ResponsePanel = ({ query, response, district, onReset }) => {
    const [weather, setWeather] = useState(null);

    useEffect(() => {
        const fetchWeather = async () => {
            const data = await api.getWeather(district);
            if (data) setWeather(data);
        };
        fetchWeather();
    }, [district]);

    return (
        <div className="w-full max-w-5xl mx-auto mt-8 animate-fade-in-up">
            <div className="bg-white dark:bg-surface-dark rounded-2xl shadow-lg border border-gray-200 dark:border-white/10 overflow-hidden flex flex-col lg:flex-row">
                {/* Main Content Area */}
                <div className="flex-grow p-0">
                    {/* Top Info Bar */}
                    <div className="bg-background-light dark:bg-black/20 border-b border-gray-200 dark:border-white/10 px-6 py-4 flex flex-wrap gap-4 items-center text-sm">
                        <div className="flex items-center text-gray-700 dark:text-gray-300">
                            <span className="material-icons text-gray-400 mr-2 text-base">place</span>
                            District: <span className="font-semibold ml-1 text-gray-900 dark:text-white">{district}</span>
                        </div>
                        <div className="h-4 w-px bg-gray-300 dark:bg-white/10 hidden sm:block"></div>
                        <div className="flex items-center text-gray-700 dark:text-gray-300">
                            <span className="material-icons text-blue-400 mr-2 text-base">cloud</span>
                            Weather: <span className="font-semibold ml-1 text-gray-900 dark:text-white">
                                {weather ? `${weather.weather}, ${weather.temp}°C` : 'Loading...'}
                            </span>
                        </div>
                        <button onClick={onReset} className="ml-auto text-xs text-primary-dark hover:underline">
                            New Search
                        </button>
                    </div>

                    {/* AI Advice Content */}
                    <div className="p-6 md:p-8">
                        <div className="flex items-start gap-4 mb-6">
                            <div className="h-10 w-10 rounded-full bg-primary/20 flex-shrink-0 flex items-center justify-center text-primary-dark dark:text-primary">
                                <span className="material-icons">smart_toy</span>
                            </div>
                            <div>
                                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1">AI Response</h3>
                                <p className="text-sm text-text-muted dark:text-gray-400">Response for: "{query}"</p>
                            </div>
                        </div>

                        <div className="prose dark:prose-invert max-w-none text-gray-800 dark:text-gray-200 whitespace-pre-wrap">
                            {response}
                        </div>

                        <div className="mt-6 flex gap-3">
                            <button className="px-4 py-2 bg-gray-100 dark:bg-white/5 hover:bg-gray-200 dark:hover:bg-white/10 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 transition-colors flex items-center cursor-pointer">
                                <span className="material-icons text-sm mr-2">volume_up</span>
                                Listen
                            </button>
                            <button className="px-4 py-2 bg-gray-100 dark:bg-white/5 hover:bg-gray-200 dark:hover:bg-white/10 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 transition-colors flex items-center cursor-pointer">
                                <span className="material-icons text-sm mr-2">share</span>
                                Share
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResponsePanel;
