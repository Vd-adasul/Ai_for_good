import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';

const ChatPanel = ({ district, onReset, selectedDistrict, initialQuery }) => {
    const [messages, setMessages] = useState([
        {
            role: 'ai',
            content: `नमस्कार! मी आपला शेती मित्र आहे. मी तुम्हाला ${district} जिल्ह्यासाठी कशी मदत करू शकतो? (Hello! I am your farming friend. How can I help you with ${district} district?)`
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    // Auto-scroll to bottom of chat
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Handle initial query if provided (when transitioning from Hero)
    const hasInitialQueryRun = useRef(false);

    // Define send logic outside handleSend to reuse
    const sendMessage = async (text) => {
        if (!text.trim()) return;

        const userMessage = { role: 'user', content: text };
        setMessages(prev => [...prev, userMessage]);
        setIsLoading(true);

        try {
            const historyPayload = messages.map(msg => ({
                role: msg.role,
                content: msg.content
            }));

            const response = await import('../services/api').then(module =>
                module.api.chat(text, district, historyPayload)
            );

            const aiMessage = { role: 'ai', content: response.response };
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            console.error("Chat error:", error);
            setMessages(prev => [...prev, {
                role: 'ai',
                content: "क्षमस्व, काहीतरी चूक झाली. कृपया पुन्हा प्रयत्न करा. (Sorry, something went wrong. Please try again.)"
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (initialQuery && !hasInitialQueryRun.current) {
            hasInitialQueryRun.current = true;
            sendMessage(initialQuery);
        }
    }, [initialQuery]);

    // Reset chat when district changes (optional, or keep history)
    useEffect(() => {
        setMessages([
            {
                role: 'ai',
                content: `नमस्कार! मी आपला शेती मित्र आहे. मी तुम्हाला ${district} जिल्ह्यासाठी कशी मदत करू शकतो?`
            }
        ]);
        hasInitialQueryRun.current = false; // Reset for new district if needed
    }, [district]);

    const handleSend = async (e) => {
        e.preventDefault();
        sendMessage(input);
        setInput('');
    };

    return (
        <div className="w-full max-w-5xl mx-auto mt-4 h-[600px] flex flex-col bg-white dark:bg-surface-dark rounded-2xl shadow-lg border border-gray-200 dark:border-white/10 overflow-hidden">
            {/* Header */}
            <div className="bg-background-light dark:bg-black/20 border-b border-gray-200 dark:border-white/10 px-6 py-4 flex justify-between items-center">
                <div className="flex items-center gap-2">
                    <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center text-primary-dark dark:text-primary">
                        <span className="material-icons text-sm">smart_toy</span>
                    </div>
                    <div>
                        <h3 className="font-bold text-gray-900 dark:text-white text-sm">AI Krishi Sahayak</h3>
                        <p className="text-xs text-text-muted dark:text-gray-400">Online • {district}</p>
                    </div>
                </div>
                <button onClick={onReset} className="text-xs text-red-500 hover:underline">
                    End Chat
                </button>
            </div>

            {/* Messages Area */}
            <div className="flex-grow overflow-y-auto p-4 space-y-4 bg-gray-50 dark:bg-black/5">
                {messages.map((msg, index) => (
                    <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] rounded-2xl p-4 ${msg.role === 'user'
                            ? 'bg-primary text-black rounded-tr-none'
                            : 'bg-white dark:bg-surface-dark border border-gray-100 dark:border-white/5 text-gray-800 dark:text-gray-200 rounded-tl-none shadow-sm'
                            }`}>
                            {msg.role === 'ai' ? (
                                <div className="prose dark:prose-invert prose-sm max-w-none">
                                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                                </div>
                            ) : (
                                <p className="whitespace-pre-wrap">{msg.content}</p>
                            )}
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-white dark:bg-surface-dark border border-gray-100 dark:border-white/5 p-4 rounded-2xl rounded-tl-none shadow-sm flex items-center gap-2">
                            <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                            <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"></span>
                            <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-300"></span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <form onSubmit={handleSend} className="p-4 bg-white dark:bg-surface-dark border-t border-gray-200 dark:border-white/10 flex gap-2">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="विचार करा... (Type your question...)"
                    className="flex-grow p-3 bg-gray-100 dark:bg-black/20 rounded-xl border-none focus:ring-2 focus:ring-primary/50 outline-none text-gray-900 dark:text-white"
                />
                <button
                    type="submit"
                    disabled={isLoading || !input.trim()}
                    className="p-3 bg-primary hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed text-black rounded-xl transition-colors flex items-center justify-center shadow-lg shadow-primary/20"
                >
                    <span className="material-icons">send</span>
                </button>
            </form>
        </div>
    );
};

export default ChatPanel;
