import React, { useState } from 'react';

const Header = ({ districts, selectedDistrict, setSelectedDistrict }) => {
    const [showDistrictList, setShowDistrictList] = useState(false);

    return (
        <header className="sticky top-0 z-50 border-b border-gray-200 dark:border-white/10 glass-effect">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-20">
                    {/* Logo & Brand */}
                    <a href="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
                        <div className="h-10 w-10 bg-primary/20 rounded-lg flex items-center justify-center text-primary-dark dark:text-primary">
                            <span className="material-icons">agriculture</span>
                        </div>
                        <div>
                            <h1 className="text-xl font-bold tracking-tight text-gray-900 dark:text-white">AI Krishi Sahayak</h1>
                            <p className="text-xs text-text-muted dark:text-gray-400">Agricultural Intelligence for Maharashtra</p>
                        </div>
                    </a>

                    {/* Location Selector */}
                    <div className="hidden md:flex items-center bg-white dark:bg-surface-dark px-4 py-2 rounded-full border border-gray-200 dark:border-white/10 shadow-sm relative">
                        <span className="material-icons text-red-500 mr-2 text-lg">place</span>
                        <span className="text-sm font-medium text-gray-600 dark:text-gray-300">Selected District:</span>
                        <span className="ml-2 text-sm font-bold text-gray-900 dark:text-white">{selectedDistrict}</span>
                        <button
                            onClick={() => setShowDistrictList(!showDistrictList)}
                            className="ml-3 text-primary-dark dark:text-primary hover:underline text-xs font-medium focus:outline-none"
                        >
                            Change
                        </button>

                        {showDistrictList && (
                            <div className="absolute top-full right-0 mt-2 w-48 bg-white dark:bg-surface-dark rounded-xl shadow-lg border border-gray-200 dark:border-white/10 overflow-hidden z-50">
                                {districts.map((district) => (
                                    <button
                                        key={district}
                                        onClick={() => {
                                            setSelectedDistrict(district);
                                            setShowDistrictList(false);
                                        }}
                                        className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5 transition-colors ${selectedDistrict === district
                                            ? 'text-primary font-bold bg-primary/5'
                                            : 'text-gray-700 dark:text-gray-200'
                                            }`}
                                    >
                                        {district}
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* WhatsApp CTA */}
                    <div className="flex items-center gap-4">
                        <div className="hidden lg:flex flex-col items-end text-right mr-2">
                            <span className="text-xs font-semibold text-gray-900 dark:text-white">Try on WhatsApp</span>
                            <span className="text-[10px] text-text-muted">+14155238886</span>
                        </div>
                        <div className="h-10 w-10 bg-white p-1 rounded-lg border border-gray-200 dark:border-white/10 shadow-sm relative group cursor-pointer overflow-hidden">
                            <img
                                alt="WhatsApp QR Code"
                                className="w-full h-full object-contain opacity-80 group-hover:opacity-100 transition-opacity"
                                src="https://lh3.googleusercontent.com/aida-public/AB6AXuCPIZ6tGjVZdRtMynz8FaSszYYSgszgkwE8hBBHrMPAQ7TokkMocPZNHglPNqmVnvOXXed2ZX2U3mW2rTBrGGE6aDSW22Jy13uiDG6jl0sr8bikJQ3BfeN0NRua_eMtIk47KUGLoHQ-92FLPtEK_LeaenDwgvIAuqyl-GPjVE4vsiKAG-N964eatX942-BDBqlt_BKmur0liIcYtFMMAbm9Vf-l8H-HXkT67YchdwTf_y_cOFqGCQfVgrKZfwbzjO2nmbkkr56zZDw"
                            />
                            <div className="absolute inset-0 bg-primary/10 group-hover:bg-transparent transition-colors"></div>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header;
