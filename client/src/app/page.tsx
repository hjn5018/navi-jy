'use client';

import React, { useState, useEffect } from 'react';

export default function Home() {
  const [micActive, setMicActive] = useState(false);
  const [time, setTime] = useState('--:--:--');

  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date();
      setTime(now.toLocaleTimeString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="p-4 h-screen max-h-screen overflow-hidden flex flex-col">
      <main className="flex-1 flex flex-col rounded-3xl overflow-hidden border border-[var(--border)] bg-white/95 backdrop-blur-md shadow-[var(--shadow)]">
        
        {/* Title Bar */}
        <header className="h-[54px] flex items-center justify-between px-[18px] bg-gradient-to-b from-[#1a5fa8] to-[#1565c0] border-b border-[rgba(21,101,192,0.3)] text-white">
          <div className="flex items-center gap-3">
            <div className="flex gap-1.5">
              <button className="w-3 h-3 rounded-full bg-[#ff5f57] border-none" title="Close" />
              <button className="w-3 h-3 rounded-full bg-[#febc2e] border-none" title="Minimize" />
              <button className="w-3 h-3 rounded-full bg-[#28c840] border-none" title="Maximize" />
            </div>
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-sm flex items-center justify-center bg-white shadow-lg text-lg">🎙</div>
              <div className="flex flex-col leading-tight">
                <span className="text-[13px] font-black tracking-wider">Voice Navigator</span>
                <span className="text-[11px] text-white/70 font-mono">NAVI Agent Core v1.0</span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button className="text-[12px] font-extrabold text-white/85 hover:underline decoration-white">단축키 보기</button>
            <span className="text-[12px] text-white/70 font-mono italic">{time}</span>
          </div>
        </header>

        {/* Status Bar */}
        <div className="grid grid-cols-4 gap-4 p-4.5 bg-gradient-to-b from-white/90 to-[#f5f9ff]/85 border-b border-[var(--border)] h-[122px]">
          <div className="sb-card">
            <span className="text-[10px] font-extrabold tracking-widest uppercase text-[var(--dim)]">마이크 상태</span>
            <div className="flex items-center gap-2 text-[14px] font-extrabold">
              <span className={`w-2.5 h-2.5 rounded-full ${micActive ? 'bg-[#1b7d3e] shadow-[0_0_8px_rgba(27,125,62,0.55)]' : 'bg-[#7a8fa8]'}`} />
              <div className={`flex items-end gap-[3px] h-[18px] ${micActive ? 'opacity-100' : 'opacity-30'}`}>
                {[...Array(7)].map((_, i) => (
                  <div key={i} className="w-[3px] h-1 rounded-sm bg-[var(--success)]" />
                ))}
              </div>
              <span className="truncate">{micActive ? '청취 중' : '대기'}</span>
            </div>
          </div>
          <div className="sb-card">
            <span className="text-[10px] font-extrabold tracking-widest uppercase text-[var(--dim)]">현재 모드</span>
            <div className="flex items-center">
              <span className="inline-flex items-center px-2.5 py-1 rounded-full text-[12px] font-extrabold text-[#0d47a1] bg-[rgba(21,101,192,0.12)] border-1.5 border-[rgba(21,101,192,0.35)]">일반 모드</span>
            </div>
          </div>
          <div className="sb-card">
            <span className="text-[10px] font-extrabold tracking-widest uppercase text-[var(--dim)]">활성 프로그램</span>
            <div className="flex items-center gap-2 text-[14px] font-extrabold">
              <span className="w-2.5 h-2.5 rounded-full bg-[#1565c0] shadow-[0_0_8px_rgba(21,101,192,0.55)]" />
              <span className="truncate">NAVI Client</span>
            </div>
          </div>
          <div className="sb-card">
            <span className="text-[10px] font-extrabold tracking-widest uppercase text-[var(--dim)]">자동화 라우터</span>
            <div className="flex items-center gap-2 text-[14px] font-extrabold">
              <span className="w-2.5 h-2.5 rounded-full bg-[#b45c00] shadow-[0_0_8px_rgba(180,92,0,0.55)]" />
              <span className="truncate">Playwright Ready</span>
            </div>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="flex-1 flex overflow-hidden">
          {/* Sidebar */}
          <aside className="w-[260px] border-r border-[var(--border)] bg-gradient-to-b from-[#f0f6ff]/98 to-[#ebf3ff]/96 p-4.5 overflow-y-auto">
            <h3 className="px-1 mb-2.5 text-[10px] font-extrabold tracking-widest uppercase text-[var(--dim)]">주요 기능</h3>
            <div className="space-y-2.5">
              <button className="cmd-btn" onClick={() => setMicActive(!micActive)}>
                <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-[var(--success-soft)] text-lg">🎙</div>
                <div className="flex-1">
                  <div className="text-[15px] font-black">{micActive ? '중지' : '듣기 시작'}</div>
                  <div className="text-[11px] text-[var(--muted)]">음성 조작 (F2)</div>
                </div>
                <kbd className="text-[10px] font-black px-1.5 py-1 rounded-full border border-[var(--border-strong)] bg-white/5 text-[var(--muted)]">F2</kbd>
              </button>
            </div>
          </aside>

          {/* Center Chat/Log Section */}
          <section className="flex-1 flex flex-col bg-gradient-to-b from-white/95 to-[#f8fcff]/90 min-w-0">
            <header className="h-[64px] border-b border-[var(--border)] px-4 py-3 flex justify-between items-center bg-white/50">
              <div>
                <h2 className="text-[18px] font-black">NAVI 컨텍스트</h2>
                <p className="text-[12px] text-[var(--muted)]">음성 명령 분석 및 작업 수행 로그</p>
              </div>
            </header>
            
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              <div className="max-w-[85%] self-end ml-auto bg-gradient-to-b from-[#1565c0]/10 to-[#1565c0]/05 border border-[rgba(21,101,192,0.25)] rounded-2xl p-3.5 shadow-sm">
                <span className="text-[10px] font-extrabold text-[var(--accent)] block mb-1.5">USER</span>
                <p className="text-[14px] leading-relaxed">유튜브에서 고양이 춤추는 영상 찾아줘</p>
              </div>
              <div className="max-w-[85%] bg-gradient-to-b from-[#1b7d3e]/08 to-[#1b7d3e]/03 border border-[rgba(27,125,62,0.18)] rounded-2xl p-3.5 shadow-sm">
                <span className="text-[10px] font-extrabold text-[var(--success)] block mb-1.5">SYSTEM</span>
                <p className="text-[14px] leading-relaxed">YouTube 브라우저 구동 중... 결과 파싱 중...</p>
              </div>
            </div>

            <footer className="h-[62px] border-top border-[var(--border)] px-4 py-2.5 flex items-center gap-3 bg-[#f0f6ff]/98">
              <input type="text" placeholder="명령어를 입력하거나 F2를 누르세요..." className="flex-1 px-4 py-3 rounded-xl border-1.5 border-[var(--border-strong)] bg-white text-[14px] outline-none focus:border-[rgba(21,101,192,0.5)] focus:ring-4 focus:ring-[rgba(21,101,192,0.12)] placeholder-[var(--dim)]" />
              <button className="w-11 h-11 rounded-xl bg-gradient-to-b from-[#1a73e8] to-[#1565c0] text-white text-lg flex items-center justify-center shadow-lg">➤</button>
            </footer>
          </section>

          {/* Right Panel (Optional Information) */}
          <aside className="w-[280px] border-l border-[var(--border)] bg-gradient-to-b from-[#f0f6ff]/98 to-[#ebf3ff]/96 p-3.5 overflow-y-auto">
            <div className="border border-[var(--border)] bg-gradient-to-b from-white to-[#f5f8fc] rounded-2xl p-3.5 shadow-sm">
              <div className="flex justify-between items-center mb-2.5">
                <span className="text-[13px] font-black">AI 통계</span>
                <span className="text-[11px] text-[var(--muted)]">v1.0.1</span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-[12px] border-b border-[rgba(21,101,192,0.08)] py-2">
                  <span className="text-[var(--muted)]">LLM Token</span>
                  <span className="font-extrabold">1,245</span>
                </div>
                <div className="flex justify-between text-[12px] py-2">
                  <span className="text-[var(--muted)]">Latency</span>
                  <span className="font-extrabold text-[#1b7d3e]">1.2s</span>
                </div>
              </div>
            </div>
          </aside>
        </div>

        {/* Global Footer */}
        <footer className="h-[42px] grid grid-cols-4 gap-2.5 px-3 py-2 bg-[#dde8f4] border-t border-[var(--border)]">
          <div className="flex items-center gap-2 px-2.5 bg-white/70 rounded-lg border border-[var(--border)]">
            <span className="text-[10px] font-extrabold text-[var(--dim)] uppercase">CPU</span>
            <span className="text-[11px] font-mono font-extrabold text-[#1b7d3e]">4.2%</span>
          </div>
          <div className="flex items-center gap-2 px-2.5 bg-white/70 rounded-lg border border-[var(--border)]">
            <span className="text-[10px] font-extrabold text-[var(--dim)] uppercase">MEM</span>
            <span className="text-[11px] font-mono font-extrabold text-[#b45c00]">256MB</span>
          </div>
        </footer>

      </main>
    </div>
  );
}
