'use client';

import { useState, useEffect } from 'react';

export default function AdminDashboard() {
  const [metrics, setMetrics] = useState<any>(null);
  const [aiTraces, setAiTraces] = useState<any[]>([]);
  const [liveBookings, setLiveBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      
      // Fetch metrics
      const metricsRes = await fetch('http://localhost:8000/api/admin/dashboard', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const metricsData = await metricsRes.json();
      setMetrics(metricsData);

      // Fetch AI traces
      const tracesRes = await fetch('http://localhost:8000/api/admin/ai-traces?limit=10', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const tracesData = await tracesRes.json();
      setAiTraces(tracesData.traces);

      // Fetch live bookings
      const bookingsRes = await fetch('http://localhost:8000/api/admin/bookings/live', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const bookingsData = await bookingsRes.json();
      setLiveBookings(bookingsData.live_bookings);

      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-2xl text-teal-400">Loading Dashboard...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            📊 Admin Dashboard
          </h1>
          <p className="text-slate-400">
            Real-time monitoring • AI traces • Live bookings
          </p>
        </div>

        {/* Metrics Grid */}
        <div className="grid md:grid-cols-4 gap-4 mb-8">
          <div className="bg-gradient-to-br from-teal-500 to-teal-600 rounded-xl p-6 shadow-lg">
            <div className="text-teal-100 text-sm mb-1">Total Bookings</div>
            <div className="text-4xl font-bold text-white">
              {metrics?.total_bookings || 0}
            </div>
          </div>

          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 shadow-lg">
            <div className="text-blue-100 text-sm mb-1">Active Now</div>
            <div className="text-4xl font-bold text-white">
              {metrics?.active_bookings || 0}
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 shadow-lg">
            <div className="text-purple-100 text-sm mb-1">Total Providers</div>
            <div className="text-4xl font-bold text-white">
              {metrics?.total_providers || 0}
            </div>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 shadow-lg">
            <div className="text-green-100 text-sm mb-1">Total Revenue</div>
            <div className="text-4xl font-bold text-white">
              PKR {metrics?.total_revenue?.toFixed(0) || 0}
            </div>
          </div>
        </div>

        {/* Service Breakdown */}
        {metrics?.service_breakdown && metrics.service_breakdown.length > 0 && (
          <div className="bg-slate-800 rounded-xl p-6 mb-8 shadow-lg">
            <h2 className="text-xl font-bold text-white mb-4">
              📈 Service Breakdown
            </h2>
            <div className="grid md:grid-cols-3 gap-4">
              {metrics.service_breakdown.map((service: any, i: number) => (
                <div key={i} className="bg-slate-700 rounded-lg p-4">
                  <div className="text-slate-300 text-sm capitalize">
                    {service.service_type.replace('_', ' ')}
                  </div>
                  <div className="text-2xl font-bold text-white">
                    {service.count} bookings
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-6">
          {/* Live Bookings */}
          <div className="bg-slate-800 rounded-xl p-6 shadow-lg">
            <h2 className="text-xl font-bold text-white mb-4">
              🔴 Live Bookings
            </h2>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {liveBookings.length === 0 ? (
                <p className="text-slate-400">No active bookings</p>
              ) : (
                liveBookings.map((booking) => (
                  <div key={booking.id} className="bg-slate-700 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <div className="text-white font-semibold">
                          #{booking.booking_number}
                        </div>
                        <div className="text-slate-300 text-sm capitalize">
                          {booking.service_type.replace('_', ' ')}
                        </div>
                      </div>
                      <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        booking.status === 'confirmed' ? 'bg-green-500 text-white' :
                        booking.status === 'en_route' ? 'bg-blue-500 text-white' :
                        'bg-yellow-500 text-white'
                      }`}>
                        {booking.status}
                      </div>
                    </div>
                    <div className="text-slate-400 text-sm">
                      Customer: {booking.customer_name}
                    </div>
                    <div className="text-slate-400 text-sm">
                      Provider: {booking.provider_name || 'Assigning...'}
                    </div>
                    <div className="text-teal-400 font-semibold mt-2">
                      PKR {booking.final_price}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* AI Traces */}
          <div className="bg-slate-800 rounded-xl p-6 shadow-lg">
            <h2 className="text-xl font-bold text-white mb-4">
              🤖 AI Reasoning Traces
            </h2>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {aiTraces.length === 0 ? (
                <p className="text-slate-400">No traces yet</p>
              ) : (
                aiTraces.map((trace) => (
                  <div key={trace.id} className="bg-slate-700 rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <div className="text-teal-400 font-semibold text-sm">
                        {trace.agent_name.replace('_', ' ').toUpperCase()}
                      </div>
                      <div className="text-slate-400 text-xs">
                        {trace.execution_time_ms}ms
                      </div>
                    </div>
                    <div className="text-slate-300 text-xs mb-1">
                      Booking: #{trace.booking_number}
                    </div>
                    <div className="space-y-1">
                      {trace.reasoning_steps.slice(0, 2).map((step: string, i: number) => (
                        <div key={i} className="text-slate-400 text-xs">
                          → {step}
                        </div>
                      ))}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Auto-refresh indicator */}
        <div className="mt-6 text-center">
          <div className="inline-flex items-center gap-2 bg-slate-800 px-4 py-2 rounded-full">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-slate-400 text-sm">Auto-refreshing every 5 seconds</span>
          </div>
        </div>
      </div>
    </div>
  );
}
