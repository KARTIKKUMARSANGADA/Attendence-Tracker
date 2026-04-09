'use client';

import { useState, useEffect, useRef } from 'react';

interface AttendanceSummary {
  id: number;
  date: string;
  status: string;
  effective_seconds: number;
  gross_seconds: number;
  break_seconds: number;
  clock_in?: string;
  clock_out?: string;
}

interface StatusResponse {
  status: string;
  record: AttendanceSummary | null;
  server_time: string;
  target_seconds: number;
}

const TARGET_SECONDS = 28800; // 8 Hours

export default function AttendanceDashboard() {
  const [data, setData] = useState<StatusResponse | null>(null);
  const [history, setHistory] = useState<AttendanceSummary[]>([]);
  const [liveEffective, setLiveEffective] = useState(0);
  const [liveGross, setLiveGross] = useState(0);
  const [loading, setLoading] = useState(true);

  const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api';

  const fetchStatus = async () => {
    try {
      const res = await fetch(`${apiBase}/status`);
      const statusData: StatusResponse = await res.json();
      setData(statusData);
      
      if (statusData.record) {
        setLiveEffective(statusData.record.effective_seconds);
        setLiveGross(statusData.record.gross_seconds);
      }
    } catch (error) {
      console.error('Failed to fetch status:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/history`);
      const historyData = await res.json();
      setHistory(historyData);
    } catch (error) {
      console.error('Failed to fetch history:', error);
    }
  };

  useEffect(() => {
    fetchStatus();
    fetchHistory();
    const interval = setInterval(fetchStatus, 30000); // Sync every 30s
    return () => clearInterval(interval);
  }, []);

  // Live Timer Logic
  useEffect(() => {
    if (data?.status === 'Working') {
      const timer = setInterval(() => {
        setLiveEffective(prev => prev + 1);
        setLiveGross(prev => prev + 1);
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [data?.status]);

  const handleAction = async () => {
    const endpoint = data?.status === 'Working' ? '/check-out' : '/check-in';
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, { method: 'POST' });
      const updatedRecord = await res.json();
      fetchStatus();
      fetchHistory();
    } catch (error) {
      alert('Action failed. Please try again.');
    }
  };

  const formatDuration = (seconds: number) => {
    const h = Math.floor(seconds / 3600).toString().padStart(2, '0');
    const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${h}:${m}:${s}`;
  };

  const formatTime = (dateStr?: string) => {
    if (!dateStr) return '—';
    return new Date(dateStr).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getHinglishQuote = (record: AttendanceSummary) => {
    const effective = record.effective_seconds;
    if (effective >= TARGET_SECONDS) return "Kya baat hai! Boss khush! 💪";
    if (effective > 0) return "Chalo koi na, kal try karenge 😅";
    return "Punch kiya tha ya nahi? 🤔";
  };

  const remaining = Math.max(0, TARGET_SECONDS - liveEffective);
  const completionEst = new Date(Date.now() + remaining * 1000);
  const progressPercent = Math.min(100, (liveEffective / TARGET_SECONDS) * 100);

  if (loading) return <div style={{color: 'white'}}>Loading Dashboard...</div>;

  return (
    <main>
      <header>
        <div>
          <h1>Attendance</h1>
          <p style={{color: 'var(--text-muted)', fontSize: '0.875rem'}}>Intern Dashboard · Target: 8h</p>
        </div>
      </header>

      <section className="glass-card">
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
          <h2 style={{fontSize: '0.875rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--text-muted)'}}>
            Today · {new Date().toLocaleDateString()}
          </h2>
          <div className={`status-badge ${data?.status === 'Working' ? 'status-working' : 'status-break'}`}>
            {data?.status || 'Not Started'}
          </div>
        </div>

        <div className="today-grid">
          <div className="stat-group">
            <div className="mini-stat">
              <span className="stat-label">Clock In</span>
              <span className="stat-value">{formatTime(data?.record?.clock_in)}</span>
            </div>
            <div className="mini-stat">
              <span className="stat-label">Clock Out</span>
              <span className="stat-value">{formatTime(data?.record?.clock_out)}</span>
            </div>
            <div className="mini-stat">
              <span className="stat-label">Break Time</span>
              <span className="stat-value">{formatDuration(data?.record?.break_seconds || 0)}</span>
            </div>
          </div>

          <div className="center-panel">
            <div className="stat-label">Effective Hours</div>
            <div className={`timer-display ${data?.status === 'Working' ? 'timer-pulsing' : ''}`}>
              {formatDuration(liveEffective)}
            </div>
            <div className="progress-container">
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ width: `${progressPercent}%` }}
                ></div>
              </div>
              <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', marginTop: '0.5rem', color: 'var(--text-muted)'}}>
                <span>Progress: {Math.round(progressPercent)}%</span>
                <span>Goal: 8h</span>
              </div>
            </div>
          </div>

          <div className="stat-group">
            <div className="mini-stat">
              <span className="stat-label">Remaining</span>
              <span className="stat-value">{formatDuration(remaining)}</span>
            </div>
            <div className="mini-stat">
              <span className="stat-label">Est. Completion</span>
              <span className="stat-value">{remaining > 0 ? formatTime(completionEst.toISOString()) : 'Done'}</span>
            </div>
            <div className="mini-stat">
              <span className="stat-label">Gross Hours</span>
              <span className="stat-value">{formatDuration(liveGross)}</span>
            </div>
          </div>
        </div>

        <button 
          onClick={handleAction}
          className={`btn ${data?.status === 'Working' ? 'btn-break' : 'btn-primary'}`}
        >
          {data?.status === 'Working' ? 'Clock Out (Take Break)' : 'Clock In (Resume)'}
        </button>
      </section>

      <section className="glass-card" style={{padding: '1.5rem'}}>
        <h2 style={{fontSize: '1rem', fontWeight: 800, marginBottom: '1.5rem', letterSpacing: '0.05em', textTransform: 'uppercase', color: 'var(--text-muted)'}}>
          Recent History
        </h2>
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Effective</th>
                <th>Gross</th>
                <th>Break</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {history.map((record) => (
                <tr key={record.id}>
                  <td style={{fontWeight: 700, color: '#fff'}}>{new Date(record.date).toLocaleDateString()}</td>
                  <td>{formatDuration(record.effective_seconds)}</td>
                  <td>{formatDuration(record.gross_seconds)}</td>
                  <td>{formatDuration(record.break_seconds)}</td>
                  <td>
                    <div className="tooltip-trigger">
                      <span className="status-badge history-status" style={{background: 'rgba(255,255,255,0.05)', color: 'var(--text)'}}>
                        {record.effective_seconds >= TARGET_SECONDS ? 'TARGET MET' : 'WORKED'}
                      </span>
                      <div className="tooltip">{getHinglishQuote(record)}</div>
                    </div>
                  </td>
                </tr>
              ))}
              {history.length === 0 && (
                <tr>
                  <td colSpan={5} style={{textAlign: 'center', color: 'var(--text-muted)', padding: '2rem'}}>
                    No history yet. Start your journey today!
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
