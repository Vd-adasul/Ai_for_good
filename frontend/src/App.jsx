import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HeroSection from './components/HeroSection';
import ChatPanel from './components/ChatPanel';
import Sidebar from './components/Sidebar';
import AdminPage from './pages/AdminPage';

function MainPage() {
  const [district, setDistrict] = useState('Beed');
  const [isChatActive, setIsChatActive] = useState(false);
  const [initialQuery, setInitialQuery] = useState('');

  const handleSearch = (searchQuery) => {
    setInitialQuery(searchQuery);
    setIsChatActive(true);
  };

  const handleReset = () => {
    setIsChatActive(false);
    setInitialQuery('');
  };

  return (
    <div className="bg-background-light dark:bg-background-dark text-text-main dark:text-white min-h-screen flex flex-col font-display selection:bg-primary selection:text-black">
      <Header
        districts={['Beed', 'Latur', 'Nashik', 'Pune', 'Nagpur']}
        selectedDistrict={district}
        setSelectedDistrict={setDistrict}
      />

      <main className="flex-grow flex flex-col items-center justify-start pt-12 pb-20 px-4 sm:px-6 relative overflow-hidden w-full">
        {/* Abstract Background Pattern */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 opacity-30 pointer-events-none">
          <div className="absolute -top-[20%] -right-[10%] w-[600px] h-[600px] bg-primary/20 rounded-full blur-3xl mix-blend-multiply dark:mix-blend-screen"></div>
          <div className="absolute top-[10%] -left-[10%] w-[400px] h-[400px] bg-yellow-100 dark:bg-yellow-900/20 rounded-full blur-3xl mix-blend-multiply dark:mix-blend-screen"></div>
        </div>

        {!isChatActive ? (
          <HeroSection
            onSearch={handleSearch}
            selectedDistrict={district}
            setSelectedDistrict={setDistrict}
            districts={['Beed', 'Latur', 'Nashik', 'Pune', 'Nagpur']}
          />
        ) : (
          <div className="flex flex-col lg:flex-row gap-6 w-full max-w-7xl animate-fade-in-up">
            <div className="flex-grow">
              <ChatPanel
                district={district}
                onReset={handleReset}
                initialQuery={initialQuery}
              />
            </div>
            <Sidebar />
          </div>
        )}

      </main>

      <Footer />
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
