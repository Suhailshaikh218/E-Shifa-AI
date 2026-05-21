'use client';

import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 via-blue-50 to-purple-50">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-teal-600 to-blue-600 mb-4">
            🏥 E-SHIFA AI
          </h1>
          <p className="text-2xl text-slate-700 mb-3 font-semibold">
            AI-Powered Home Healthcare Service Orchestrator
          </p>
          <p className="text-lg text-slate-600 mb-6">
            For Pakistan's Informal Economy • Multilingual • Intelligent Matching
          </p>
          
          <div className="flex justify-center gap-4">
            <Link href="/book">
              <button className="bg-gradient-to-r from-teal-600 to-blue-600 text-white px-8 py-4 rounded-lg font-bold text-lg hover:from-teal-700 hover:to-blue-700 transition-all shadow-lg">
                🚀 Book Service Now
              </button>
            </Link>
            
            <Link href="/auth">
              <button className="bg-white text-teal-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-slate-50 transition-all shadow-lg border-2 border-teal-600">
                👤 Sign In
              </button>
            </Link>
          </div>
        </div>

        {/* Services Grid */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-slate-800 text-center mb-8">
            Our Services
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              { icon: '👩‍⚕️', name: 'Home Nurse', desc: 'Professional nursing care' },
              { icon: '👨‍⚕️', name: 'Doctor Visit', desc: 'Doctor at your doorstep' },
              { icon: '🤝', name: 'Caregiver', desc: 'Elderly & patient care' },
              { icon: '🏃', name: 'Physiotherapist', desc: 'Physical therapy at home' },
              { icon: '🧪', name: 'Lab Collection', desc: 'Sample pickup service' },
              { icon: '🚑', name: 'Ambulance', desc: 'Emergency transport' }
            ].map((service, i) => (
              <div key={i} className="bg-white rounded-xl shadow-md p-6 hover:shadow-xl transition-all">
                <div className="text-5xl mb-3">{service.icon}</div>
                <h3 className="text-xl font-bold text-slate-800 mb-2">{service.name}</h3>
                <p className="text-slate-600">{service.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* How It Works */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-16">
          <h2 className="text-3xl font-bold text-slate-800 text-center mb-8">
            How It Works
          </h2>
          <div className="grid md:grid-cols-5 gap-4">
            {[
              { step: '1', icon: '💬', text: 'Request Service' },
              { step: '2', icon: '🤖', text: 'AI Matches Provider' },
              { step: '3', icon: '💰', text: 'Dynamic Pricing' },
              { step: '4', icon: '✅', text: 'Instant Confirmation' },
              { step: '5', icon: '⭐', text: 'Rate & Review' }
            ].map((item, i) => (
              <div key={i} className="text-center">
                <div className="bg-teal-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                  <span className="text-2xl">{item.icon}</span>
                </div>
                <p className="font-semibold text-slate-800">{item.text}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-16">
          <div className="bg-gradient-to-br from-teal-500 to-teal-600 rounded-xl shadow-lg p-6 text-white">
            <div className="text-4xl mb-3">🤖</div>
            <h3 className="text-xl font-bold mb-2">AI-Powered Matching</h3>
            <p className="text-teal-50">10-factor algorithm for best provider selection</p>
          </div>
          
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 text-white">
            <div className="text-4xl mb-3">🌐</div>
            <h3 className="text-xl font-bold mb-2">Multilingual Support</h3>
            <p className="text-blue-50">Urdu, Roman Urdu, and English</p>
          </div>
          
          <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg p-6 text-white">
            <div className="text-4xl mb-3">💡</div>
            <h3 className="text-xl font-bold mb-2">Transparent Pricing</h3>
            <p className="text-purple-50">Dynamic pricing with full breakdown</p>
          </div>
        </div>

        {/* Admin Link */}
        <div className="text-center">
          <Link href="/admin/dashboard">
            <div className="inline-block bg-gradient-to-r from-slate-800 to-slate-900 text-white px-8 py-4 rounded-lg hover:from-slate-900 hover:to-black transition-all shadow-lg">
              <div className="flex items-center gap-3">
                <span className="text-2xl">📊</span>
                <div className="text-left">
                  <div className="font-bold text-lg">Admin Dashboard</div>
                  <div className="text-xs text-slate-300">Real-Time Metrics • AI Traces</div>
                </div>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}
