import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

const Sidebar = () => {
    const [subsidies, setSubsidies] = useState([]);
    const [prices, setPrices] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            // Mock data for subsidies for now or fetch from API
            // const subsidyData = await api.getSubsidies();
            // setSubsidies(subsidyData);

            const priceData = await api.getPrices();
            setPrices(priceData);
        };
        fetchData();
    }, []);

    return (
        <div className="lg:w-80 bg-background-light dark:bg-black/30 border-t lg:border-t-0 lg:border-l border-gray-200 dark:border-white/10 p-6 flex flex-col justify-between">
            <div>
                <div className="flex items-center gap-2 mb-4">
                    <span className="material-icons text-yellow-600">lightbulb</span>
                    <h4 className="font-bold text-gray-900 dark:text-white text-sm uppercase tracking-wide">Subsidy Suggestion</h4>
                </div>
                <div className="bg-white dark:bg-surface-dark p-4 rounded-xl border border-primary/20 shadow-sm relative overflow-hidden group">
                    <div className="absolute top-0 left-0 w-1 h-full bg-primary"></div>
                    <h5 className="font-bold text-gray-900 dark:text-white mb-2 pr-6">PMKSY Drip Irrigation Scheme</h5>
                    <span className="absolute top-2 right-2 h-6 w-6 bg-primary/10 rounded-full flex items-center justify-center text-primary-dark">
                        <span className="material-icons text-sm">north_east</span>
                    </span>
                    <p className="text-sm text-text-muted dark:text-gray-400 mb-3">Get up to <span className="font-bold text-primary-dark dark:text-primary">55% subsidy</span> for installing drip irrigation systems.</p>
                    <button className="w-full py-2 bg-primary/10 hover:bg-primary/20 text-primary-dark dark:text-primary rounded-lg text-sm font-semibold transition-colors cursor-pointer">
                        Check Eligibility
                    </button>
                </div>

                {/* Market Trend */}
                <div className="mt-6">
                    <h4 className="font-bold text-gray-900 dark:text-white text-xs uppercase tracking-wide mb-3 text-text-muted">Market Trend</h4>

                    {prices.length > 0 ? prices.map((item, index) => (
                        <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-white dark:bg-surface-dark border border-gray-100 dark:border-white/5 mb-2">
                            <div className="flex items-center gap-3">
                                <div className="h-8 w-8 rounded bg-green-100 dark:bg-green-900 flex items-center justify-center">
                                    <span className="material-icons text-green-700 dark:text-green-400 text-sm">trending_up</span>
                                </div>
                                <div className="flex flex-col">
                                    <span className="text-xs font-semibold text-gray-900 dark:text-white">{item.commodity}</span>
                                    <span className="text-[10px] text-green-600">{item.change}</span>
                                </div>
                            </div>
                            <span className="text-sm font-bold">₹{item.price}</span>
                        </div>
                    )) : (
                        <div className="text-sm text-gray-500">Loading prices...</div>
                    )}

                </div>
            </div>
        </div>
    );
};

export default Sidebar;
