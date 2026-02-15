import React, { useState } from 'react';
import axios from 'axios';
import { Upload, FileText, Plus, ShieldCheck, LogOut, FileType, CheckCircle, AlertCircle } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const AdminPage = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    // Dashboard state
    const [activeTab, setActiveTab] = useState('subsidy'); // subsidy, upload, context

    // Forms state
    const [subsidyForm, setSubsidyForm] = useState({ category: '', name: '', benefit: '', type: '' });
    const [contextText, setContextText] = useState('');
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [msg, setMsg] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);

            const res = await axios.post(`${API_BASE_URL}/admin/login`, formData);
            if (res.data.status === 'success') {
                setIsAuthenticated(true);
            }
        } catch (err) {
            setError(err.response?.data?.message || 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    const handleAddSubsidy = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const formData = new FormData();
            Object.keys(subsidyForm).forEach(key => formData.append(key, subsidyForm[key]));
            await axios.post(`${API_BASE_URL}/admin/add_scheme`, formData);
            setMsg('Subsidy Added Successfully!');
            setSubsidyForm({ category: '', name: '', benefit: '', type: '' });
        } catch (err) {
            setMsg('Error adding subsidy.');
        } finally {
            setLoading(false);
        }
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) return;
        setLoading(true);
        try {
            const formData = new FormData();
            formData.append('file', file);
            const res = await axios.post(`${API_BASE_URL}/admin/upload_district_data`, formData);
            setMsg(res.data.message);
            setFile(null);
        } catch (err) {
            setMsg('Upload failed.');
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateContext = async (e) => {
        e.preventDefault();
        if (!contextText) return;
        setLoading(true);
        try {
            const formData = new FormData();
            formData.append('context_text', contextText);
            await axios.post(`${API_BASE_URL}/admin/update_context`, formData);
            setMsg('Context Updated Successfully!');
            setContextText('');
        } catch (err) {
            setMsg('Update failed.');
        } finally {
            setLoading(false);
        }
    };

    if (!isAuthenticated) {
        return (
            <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8 font-display">
                <div className="sm:mx-auto sm:w-full sm:max-w-md">
                    <div className="flex justify-center">
                        <ShieldCheck className="h-12 w-12 text-primary" />
                    </div>
                    <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">Admin Login</h2>
                </div>

                <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
                    <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
                        <form className="space-y-6" onSubmit={handleLogin}>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Username</label>
                                <div className="mt-1">
                                    <input type="text" required value={username} onChange={(e) => setUsername(e.target.value)}
                                        className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm text-black" />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700">Password</label>
                                <div className="mt-1">
                                    <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
                                        className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm text-black" />
                                </div>
                            </div>

                            {error && <div className="text-red-500 text-sm">{error}</div>}

                            <div>
                                <button type="submit" disabled={loading}
                                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                                    {loading ? 'Logging in...' : 'Sign in'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-100 flex font-display text-text-main">
            {/* Sidebar */}
            <div className="w-64 bg-white shadow-md flex flex-col fixed h-full">
                <div className="p-6 flex items-center space-x-2 border-b">
                    <ShieldCheck className="text-primary" />
                    <h1 className="text-xl font-bold text-gray-800">Admin Panel</h1>
                </div>
                <nav className="flex-1 p-4 space-y-2">
                    <button onClick={() => setActiveTab('subsidy')}
                        className={`w-full flex items-center space-x-2 px-4 py-2 rounded-lg text-left transition-colors ${activeTab === 'subsidy' ? 'bg-primary/10 text-primary' : 'text-gray-600 hover:bg-gray-50'}`}>
                        <Plus size={20} /> <span>Add Subsidy</span>
                    </button>
                    <button onClick={() => setActiveTab('upload')}
                        className={`w-full flex items-center space-x-2 px-4 py-2 rounded-lg text-left transition-colors ${activeTab === 'upload' ? 'bg-primary/10 text-primary' : 'text-gray-600 hover:bg-gray-50'}`}>
                        <Upload size={20} /> <span>Upload District Data</span>
                    </button>
                    <button onClick={() => setActiveTab('context')}
                        className={`w-full flex items-center space-x-2 px-4 py-2 rounded-lg text-left transition-colors ${activeTab === 'context' ? 'bg-primary/10 text-primary' : 'text-gray-600 hover:bg-gray-50'}`}>
                        <FileText size={20} /> <span>RAG Context</span>
                    </button>
                </nav>
                <div className="p-4 border-t">
                    <button onClick={() => setIsAuthenticated(false)} className="w-full flex items-center space-x-2 px-4 py-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors">
                        <LogOut size={20} /> <span>Logout</span>
                    </button>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 p-8 ml-64">
                <div className="bg-white rounded-xl shadow-sm p-6 max-w-3xl mx-auto mt-10">
                    {msg && (
                        <div className={`mb-4 p-4 rounded-lg flex items-center space-x-2 animate-pulse ${msg.includes('Success') || msg.includes('processed') ? 'bg-green-50 text-green-700' : 'bg-blue-50 text-blue-700'}`}>
                            <CheckCircle size={20} />
                            <span>{msg}</span>
                            <button onClick={() => setMsg('')} className="ml-auto text-sm opacity-50 hover:opacity-100">Dismiss</button>
                        </div>
                    )}

                    {activeTab === 'subsidy' && (
                        <div>
                            <h2 className="text-2xl font-bold mb-6 text-primary">Add New Subsidy Scheme</h2>
                            <form onSubmit={handleAddSubsidy} className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Scheme Category</label>
                                    <input type="text" required value={subsidyForm.category} onChange={e => setSubsidyForm({ ...subsidyForm, category: e.target.value })}
                                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring focus:ring-primary/20 px-3 py-2 border text-black" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Scheme Name</label>
                                    <input type="text" required value={subsidyForm.name} onChange={e => setSubsidyForm({ ...subsidyForm, name: e.target.value })}
                                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring focus:ring-primary/20 px-3 py-2 border text-black" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Benefit Details</label>
                                    <textarea required value={subsidyForm.benefit} onChange={e => setSubsidyForm({ ...subsidyForm, benefit: e.target.value })}
                                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring focus:ring-primary/20 px-3 py-2 border text-black" rows="3" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Type (e.g., State/Central)</label>
                                    <input type="text" required value={subsidyForm.type} onChange={e => setSubsidyForm({ ...subsidyForm, type: e.target.value })}
                                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring focus:ring-primary/20 px-3 py-2 border text-black" />
                                </div>
                                <button type="submit" disabled={loading} className="w-full bg-primary text-white py-2 rounded-lg hover:bg-primary-dark disabled:opacity-50 transition-colors">
                                    {loading ? 'Adding...' : 'Add Scheme'}
                                </button>
                            </form>
                        </div>
                    )}

                    {activeTab === 'upload' && (
                        <div>
                            <h2 className="text-2xl font-bold mb-6 text-primary">Upload District RAG Data</h2>
                            <p className="text-gray-500 mb-4">Upload PDF files containing agricultural data for districts. These will be indexed by the RAG system immediately.</p>
                            <form onSubmit={handleUpload} className="space-y-4">
                                <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:bg-gray-50 transition-colors cursor-pointer"
                                    onClick={() => document.getElementById('file-upload').click()}>
                                    <Upload className="mx-auto h-16 w-16 text-gray-400" />
                                    <p className="mt-4 text-sm text-gray-600 font-medium">Click to upload PDF</p>
                                    <input id="file-upload" type="file" accept=".pdf" className="hidden" onChange={e => setFile(e.target.files[0])} />
                                </div>
                                {file && (
                                    <div className="bg-blue-50 p-3 rounded-lg flex items-center justify-center space-x-2">
                                        <FileText size={20} className="text-primary" />
                                        <p className="text-sm font-medium text-primary">{file.name}</p>
                                    </div>
                                )}

                                <button type="submit" disabled={loading || !file} className="w-full bg-primary text-white py-2 rounded-lg hover:bg-primary-dark disabled:opacity-50 transition-colors">
                                    {loading ? 'Processing...' : 'Upload & Index'}
                                </button>
                            </form>
                        </div>
                    )}

                    {activeTab === 'context' && (
                        <div>
                            <h2 className="text-2xl font-bold mb-6 text-primary">Update RAG Context</h2>
                            <p className="text-gray-500 mb-4">Add direct text context to the RAG system (e.g., "Monsoon delayed in Latur by 2 weeks"). This will be appended to permanent context.</p>
                            <form onSubmit={handleUpdateContext} className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Additional Context</label>
                                    <textarea required value={contextText} onChange={e => setContextText(e.target.value)}
                                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring focus:ring-primary/20 px-3 py-2 border text-black" rows="6"
                                        placeholder="Enter important context here..." />
                                </div>
                                <button type="submit" disabled={loading} className="w-full bg-primary text-white py-2 rounded-lg hover:bg-primary-dark disabled:opacity-50 transition-colors">
                                    {loading ? 'Updating...' : 'Update Context'}
                                </button>
                            </form>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AdminPage;
