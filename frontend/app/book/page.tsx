'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

const services = [
  {
    id: 'home_nurse',
    name: 'Home Nurse',
    icon: '👩‍⚕️',
    description: 'Professional nursing care at your home',
    basePrice: 1500
  },
  {
    id: 'doctor_visit',
    name: 'Doctor Home Visit',
    icon: '👨‍⚕️',
    description: 'Doctor consultation at your doorstep',
    basePrice: 3000
  },
  {
    id: 'caregiver',
    name: 'Caregiver',
    icon: '🤝',
    description: 'Elderly and patient care services',
    basePrice: 1200
  },
  {
    id: 'physiotherapist',
    name: 'Physiotherapist',
    icon: '🏃',
    description: 'Physical therapy at home',
    basePrice: 2000
  },
  {
    id: 'lab_collection',
    name: 'Lab Sample Collection',
    icon: '🧪',
    description: 'Blood/urine sample pickup',
    basePrice: 800
  },
  {
    id: 'ambulance',
    name: 'Ambulance',
    icon: '🚑',
    description: 'Emergency medical transport',
    basePrice: 2500
  }
];

export default function BookService() {
  const router = useRouter();
  const [selectedService, setSelectedService] = useState<string | null>(null);
  const [userQuery, setUserQuery] = useState('');
  const [location, setLocation] = useState({
    lat: 24.8607,
    lng: 67.0011,
    address: 'Karachi, Pakistan'
  });
  const [urgency, setUrgency] = useState('routine');
  const [loading, setLoading] = useState(false);

  const handleServiceSelect = (serviceId: string) => {
    setSelectedService(serviceId);
    const service = services.find(s => s.id === serviceId);
    setUserQuery(`I need ${service?.name.toLowerCase()} service`);
  };

  const handleBooking = async () => {
    if (!selectedService) {
      alert('Please select a service');
      return;
    }

    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      
      const response = await fetch('http://localhost:8000/api/bookings/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          user_query: userQuery,
          location: location
        })
      });

      if (!response.ok) {
        throw new Error('Booking failed');
      }

      const data = await response.json();
      
      // Redirect to booking details
      router.push(`/booking/${data.booking_id}`);
      
    } catch (error) {
      console.error('Booking error:', error);
      alert('Booking failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 to-blue-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-teal-800 mb-2">
            🏥 Book Healthcare Service
          </h1>
          <p className="text-slate-600">
            AI-powered matching • Transparent pricing • Instant confirmation
          </p>
        </div>

        {/* Service Selection */}
        {!selectedService && (
          <div>
            <h2 className="text-2xl font-bold text-slate-800 mb-4">
              Select a Service
            </h2>
            <div className="grid md:grid-cols-3 gap-4">
              {services.map((service) => (
                <div
                  key={service.id}
                  onClick={() => handleServiceSelect(service.id)}
                  className="bg-white rounded-xl shadow-md p-6 hover:shadow-xl transition-all cursor-pointer border-2 border-transparent hover:border-teal-500"
                >
                  <div className="text-5xl mb-3">{service.icon}</div>
                  <h3 className="text-xl font-bold text-slate-800 mb-2">
                    {service.name}
                  </h3>
                  <p className="text-slate-600 text-sm mb-3">
                    {service.description}
                  </p>
                  <div className="text-teal-600 font-bold">
                    From PKR {service.basePrice}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Booking Form */}
        {selectedService && (
          <div className="bg-white rounded-xl shadow-lg p-8">
            <button
              onClick={() => setSelectedService(null)}
              className="text-teal-600 mb-4 hover:underline"
            >
              ← Change Service
            </button>

            <h2 className="text-2xl font-bold text-slate-800 mb-6">
              {services.find(s => s.id === selectedService)?.icon}{' '}
              {services.find(s => s.id === selectedService)?.name}
            </h2>

            {/* User Query */}
            <div className="mb-6">
              <label className="block text-slate-700 font-semibold mb-2">
                Describe your need (Urdu/English/Roman Urdu)
              </label>
              <textarea
                value={userQuery}
                onChange={(e) => setUserQuery(e.target.value)}
                className="w-full border-2 border-slate-300 rounded-lg p-3 focus:border-teal-500 focus:outline-none"
                rows={3}
                placeholder="e.g., Mujhe ghar pe nurse chahiye kal subah 10 baje"
              />
            </div>

            {/* Location */}
            <div className="mb-6">
              <label className="block text-slate-700 font-semibold mb-2">
                Your Location
              </label>
              <input
                type="text"
                value={location.address}
                onChange={(e) => setLocation({...location, address: e.target.value})}
                className="w-full border-2 border-slate-300 rounded-lg p-3 focus:border-teal-500 focus:outline-none"
                placeholder="Enter your address"
              />
              <p className="text-xs text-slate-500 mt-1">
                Lat: {location.lat}, Lng: {location.lng}
              </p>
            </div>

            {/* Urgency */}
            <div className="mb-6">
              <label className="block text-slate-700 font-semibold mb-2">
                Urgency Level
              </label>
              <div className="flex gap-3">
                {['routine', 'urgent', 'emergency'].map((level) => (
                  <button
                    key={level}
                    onClick={() => setUrgency(level)}
                    className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                      urgency === level
                        ? 'bg-teal-600 text-white'
                        : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                    }`}
                  >
                    {level.charAt(0).toUpperCase() + level.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            {/* Book Button */}
            <button
              onClick={handleBooking}
              disabled={loading}
              className="w-full bg-gradient-to-r from-teal-600 to-blue-600 text-white py-4 rounded-lg font-bold text-lg hover:from-teal-700 hover:to-blue-700 transition-all disabled:opacity-50"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="animate-spin">⏳</span>
                  Finding Best Provider...
                </span>
              ) : (
                '🤖 Find Provider with AI'
              )}
            </button>

            {loading && (
              <div className="mt-6 bg-slate-100 rounded-lg p-4">
                <p className="text-slate-700 font-semibold mb-2">
                  🤖 AI Agents Working...
                </p>
                <div className="space-y-2 text-sm text-slate-600">
                  <p>✓ Extracting intent from your query...</p>
                  <p>✓ Matching providers using 10-factor algorithm...</p>
                  <p>✓ Calculating dynamic pricing...</p>
                  <p>✓ Checking availability and scheduling...</p>
                  <p>✓ Sending notifications...</p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
