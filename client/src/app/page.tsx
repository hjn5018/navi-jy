'use client';

import React, { useState, useEffect, useRef } from 'react';

export default function Home() {
  const [micActive, setMicActive] = useState(false);
  const [time, setTime] = useState('--:--:--');
  const [command, setCommand] = useState('');
  const [history, setHistory] = useState<{ role: string, content: string, type?: string }[]>([
    { role: 'SYSTEM', content: 'NAVI AI Agent 활성화됨. 무엇을 도와드릴까요?', type: 'log' },
  ]);
  const [loading, setLoading] = useState(false);
  const [isCompact, setIsCompact] = useState(false);
  const [wsStatus, setWsStatus] = useState('disconnected');
  const scrollRef = useRef<HTMLDivElement>(null);
  const ws = useRef<WebSocket | null>(null);

  // Initialize WebSocket
  useEffect(() => {
    const connectWS = () => {
      const socket = new WebSocket('ws://localhost:8000/ws');
      ws.current = socket;

      socket.onopen = () => {
        console.log('[*] WebSocket Connected');
        setWsStatus('connected');
      };

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('[*] WS Message:', data);
        
        if (data.type === 'status') {
          // Add a temporary status log
          setHistory(prev => [...prev, { role: 'SYSTEM', content: data.content, type: 'log' }]);
        } else if (data.type === 'result') {
          setLoading(false);
          const content = data.content.status === 'success' 
            ? String(data.content.result.content) 
            : `Error: ${data.content.message}`;
          setHistory(prev => [...prev, { role: 'NAVI', content }]);
        }
      };

      socket.onclose = () => {
        console.log('[!] WebSocket Disconnected. Retrying in 3s...');
        setWsStatus('disconnected');
        setTimeout(connectWS, 3000);
      };

      socket.onerror = (err) => {
        console.error('[!] WS Error:', err);
      };
    };

    connectWS();
    return () => ws.current?.close();
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date();
      setTime(now.toLocaleTimeString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [history]);

  const handleSendCommand = () => {
    if (!command.trim()) return;
    
    const newMsg = { role: 'USER', content: command };
    setHistory(prev => [...prev, newMsg]);
    
    if (ws.current && wsStatus === 'connected') {
      ws.current.send(JSON.stringify({ type: 'command', content: command }));
      setLoading(true);
    } else {
      setHistory(prev => [...prev, { role: 'NAVI', content: '서버와 연결되어 있지 않습니다. WebSocket 상태를 확인하세요.' }]);
    }
    setCommand('');
  };

  return (
    <div className={`p-4 transition-all duration-500 ease-in-out flex flex-col items-center justify-center ${isCompact ? 'h-auto w-[400px] fixed bottom-8 right-8' : 'h-screen w-full'}`}>
      
      <main className={`flex flex-col rounded-3xl overflow-hidden border border-[var(--border)] bg-white/95 backdrop-blur-md shadow-[var(--shadow)] transition-all ${isCompact ? 'w-full h-[600px]' : 'w-full h-full'}`}>
        
        {/* Title Bar */}
        <header className="h-[54px] flex items-center justify-between px-[18px] bg-gradient-to-b from-[#1a5fa8] to-[#1565c0] border-b border-[rgba(21,101,192,0.3)] text-white shrink-0">
          <div className="flex items-center gap-3">
            <div className="flex gap-1.5">
              <button className="w-3 h-3 rounded-full bg-[#ff5f57]" />
              <button 
                onClick={() => setIsCompact(!isCompact)}
                className="w-3 h-3 rounded-full bg-[#febc2e] hover:brightness-110" 
                title={isCompact ? "Expand" : "Collapse"}
              />
              <button className="w-3 h-3 rounded-full bg-[#28c840]" />
            </div>
            {!isCompact && (
              <div className="flex items-center gap-2.5 ml-2">
                <div className="w-7 h-7 rounded-sm flex items-center justify-center bg-white shadow-lg text-lg text-black">🎙</div>
                <div className="flex flex-col leading-tight">
                  <span className="text-[13px] font-black tracking-wider">Voice Navigator</span>
                  <span className="text-[11px] text-white/70 font-mono italic">{time}</span>
                </div>
              </div>
            )}
          </div>
          {isCompact && <div className="text-[11px] font-mono mr-2">{time}</div>}
          <div className="flex items-center gap-3">
            <div className={`text-[10px] font-black px-2 py-0.5 rounded-full border ${wsStatus === 'connected' ? 'border-green-400 text-green-200 bg-green-900/30' : 'border-red-400 text-red-200 bg-red-900/30'}`}>
              {wsStatus === 'connected' ? 'LIVE' : 'OFFLINE'}
            </div>
            {!isCompact && <button className="text-[11px] font-extrabold text-white/85 hover:underline decoration-white">Settings</button>}
          </div>
        </header>

        {/* Status Mini Bar */}
        <div className={`flex gap-3 px-4 py-2.5 bg-[#f5f9ff]/85 border-b border-[var(--border)] shrink-0 overflow-x-auto no-scrollbar`}>
          <div className="flex items-center gap-2 px-3 py-1.5 bg-white border border-[var(--border)] rounded-full shadow-sm text-[11px] font-bold shrink-0">
            <span className={`w-2 h-2 rounded-full ${micActive ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`} />
            <span>MIC: {micActive ? 'ON' : 'OFF'}</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 bg-white border border-[var(--border)] rounded-full shadow-sm text-[11px] font-bold shrink-0">
            <span className={`w-2 h-2 rounded-full ${loading ? 'bg-blue-500 animate-spin' : 'bg-orange-400'}`} />
            <span>ROUTER: {loading ? 'WORK' : 'READY'}</span>
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 flex overflow-hidden">
          {/* Main Chat Log */}
          <section className="flex-1 flex flex-col min-w-0 bg-gradient-to-b from-white to-[#f8fcff]">
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4 flex flex-col scroll-smooth">
              {history.map((msg, idx) => (
                <div 
                  key={idx} 
                  className={`max-w-[85%] animate-in slide-in-from-bottom-2 duration-300 ${msg.role === 'USER' ? 'self-end ml-auto bg-[var(--accent)] text-white' : msg.type === 'log' ? 'self-stretch bg-[#f0f9ff] border border-blue-100 text-blue-800 text-center text-[12px] py-1.5' : 'self-start bg-white border border-[var(--border)]'} rounded-2xl p-3.5 shadow-sm whitespace-pre-wrap`}
                >
                  {msg.role !== 'SYSTEM' && (
                    <span className={`text-[10px] font-black block mb-1 uppercase ${msg.role === 'USER' ? 'text-white/60' : 'text-blue-500'}`}>
                      {msg.role}
                    </span>
                  )}
                  <p className="text-[14px] leading-relaxed font-medium">{msg.content}</p>
                </div>
              ))}
              {loading && (
                <div className="flex gap-2 p-2 self-start bg-white border border-gray-100 rounded-2xl shadow-sm">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-75" />
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-150" />
                </div>
              )}
            </div>

            {/* Input Footer */}
            <footer className="p-4 border-t border-[var(--border)] bg-white/50 shrink-0">
              <div className="flex items-center gap-2 bg-white border-2 border-[var(--border-strong)] rounded-2xl p-1 shadow-inner focus-within:border-blue-400 transition-colors">
                <input 
                  value={command}
                  onChange={(e) => setCommand(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSendCommand()}
                  type="text" 
                  placeholder="Ask NAVI..." 
                  className="flex-1 bg-transparent px-3 py-2 text-[14px] outline-none" 
                />
                <button 
                  onClick={handleSendCommand}
                  className="w-10 h-10 rounded-xl bg-[var(--accent)] text-white flex items-center justify-center hover:scale-105 active:scale-95 transition-transform disabled:opacity-50"
                  disabled={wsStatus !== 'connected'}
                >
                  ➤
                </button>
              </div>
            </footer>
          </section>
        </div>

      </main>

      {/* Floating Toggle Hint */}
      {!isCompact && (
        <button 
          onClick={() => setIsCompact(true)}
          className="mt-4 px-6 py-2 bg-white/30 backdrop-blur rounded-full text-[12px] font-bold border border-white/50 hover:bg-white/50 transition-all text-blue-900"
        >
          오버레이 모드로 전환 (Compact Mode)
        </button>
      )}

    </div>
  );
}
