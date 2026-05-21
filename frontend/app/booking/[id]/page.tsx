'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';

export default function BookingDetails() {
  const params = useParams();
  const bookingId = params.id;
  
  const [booking, setBooking] = useState<any>(null);
  const [aiTraces, setAiTraces] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showFeedback, setShowFeedback] = useState(false);
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');

  useEffect(() => {
    fetchBookingDetails();
  }, [bookingId]);

  const fetchBookingDetails = async () => {
    try {
      const token = localStorage.getItem('token');
      
      const response = await fetch(`http://localhost:8000/api/bookings/${bookingId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();
      setBooking(data.booking);
      setAiTraces(data.ai_traces);
    } catch (error) {
      console.error('Error fetching booking:', error);
    } finally {
      setLoading(false);
    }
  };

  const submitFeedback = async () => {
    try {
      const token = localStorage.getItem('token');
      
      const response = await fetch('http://localhost:8000/api/bookings/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          booking_id: bookingId,
          rating,
          comment
        })
      });

      if (response.ok) {
        alert('Feedback submitted successfully!');
        setShowFeedback(false);
        fetchBookingDetails();
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-teal-50 to-blue-50 flex items-center justify-center">
        <div className="text-2xl text-teal-600">Loading...</div>
      </div>
    );
  }

  if (!booking) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-teal-50 to-blue-50 flex items-center justify-center">
        <div className="text-2xl text-red-600">Booking not found</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 to-blue-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-teal-800 mb-2">
                Booking #{booking.booking_number}
              </h1>
              <p className="text-slate-600">
                {booking.service_type.replace('_', ' ').toUpperCase()}
              </p>
            </div>
            <div className={`px-4 py-2 rounded-full font-semibold ${
              booking.status === 'confirmed' ? 'bg-green-100 text-green-700' :
              booking.status === 'completed' ? 'bg-blue-100 text-blue-700' :
              'bg-yellow-100 text-yellow-700'
            }`}>
              {booking.status.toUpperCase()}
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Booking Details */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-slate-800 mb-4">
              📋 Booking Details
            </h2>
            
            <div className="space-y-3">
              <div>
                <p className="text-slate-600 text-sm">Provider</p>
                <p className="font-semibold text-slate-800">
                  {booking.provider_name || 'Assigning...'}
                </p>
              </div>
              
              <div>
                <p className="text-slate-600 text-sm">Scheduled Time</p>
                <p className="font-semibold text-slate-800">
                  {new Date(booking.scheduled_time).toLocaleString()}
                </p>
              </div>
              
              <div>
                <p className="text-slate-600 text-sm">Urgency</p>
                <p className="font-semibold text-slate-800 capitalize">
                  {booking.urgency}
                </p>
              </div>
              
              <div>
                <p className="text-slate-600 text-sm">Distance</p>
                <p className="font-semibold text-slate-800">
                  {booking.distance_km} km
                </p>
              </div>
            </div>
          </div>

          {/* Pricing Breakdown */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-slate-800 mb-4">
              💰 Pricing Breakdown
            </h2>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-600">Base Fee</span>
                <span className="font-semibold">PKR {booking.base_price}</span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-slate-600">Distance Fee</span>
                <span className="font-semibold">PKR {booking.distance_fee}</span>
              </div>
              
              {booking.urgency_surcharge > 0 && (
                <div className="flex justify-between">
                  <span className="text-slate-600">Urgency Surcharge</span>
                  <span className="font-semibold text-orange-600">
                    +PKR {booking.urgency_surcharge}
                  </span>
                </div>
              )}
              
              {booking.demand_surge > 0 && (
                <div className="flex justify-between">
                  <span className="text-slate-600">Demand Surge</span>
                  <span className="font-semibold text-orange-600">
                    +PKR {booking.demand_surge}
                  </span>
                </div>
              )}
              
              {booking.loyalty_discount > 0 && (
                <div className="flex justify-between">
                  <span className="text-slate-600">Loyalty Discount</span>
                  <span className="font-semibold text-green-600">
                    -PKR {booking.loyalty_discount}
                  </span>
                </div>
              )}
              
              <div className="border-t-2 border-slate-200 pt-2 mt-2">
                <div className="flex justify-between text-lg">
                  <span className="font-bold text-slate-800">Total</span>
                  <span className="font-bold text-teal-600">
                    PKR {booking.final_price}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* AI Reasoning Traces */}
        <div className="bg-slate-900 rounded-xl shadow-lg p-6 mt-6">
          <h2 className="text-xl font-bold text-white mb-4">
            🤖 AI Reasoning Traces
          </h2>
          
          <div className="space-y-4">
            {aiTraces.map((trace, index) => (
              <div key={index} className="bg-slate-800 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-teal-400 font-semibold">
                    {trace.agent_name.replace('_', ' ').toUpperCase()}
                  </span>
                  <span className="text-slate-400 text-sm">
                    {trace.execution_time_ms}ms
                  </span>
                </div>
                
                <div className="space-y-1">
                  {trace.reasoning_steps.map((step: string, i: number) => (
                    <p key={i} className="text-slate-300 text-sm">
                      → {step}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Feedback Section */}
        {booking.status === 'completed' && !showFeedback && (
          <div className="mt-6">
            <button
              onClick={() => setShowFeedback(true)}
              className="w-full bg-gradient-to-r from-teal-600 to-blue-600 text-white py-4 rounded-lg font-bold hover:from-teal-700 hover:to-blue-700"
            >
              ⭐ Rate Your Experience
            </button>
          </div>
        )}

        {showFeedback && (
          <div className="bg-white rounded-xl shadow-lg p-6 mt-6">
            <h2 className="text-xl font-bold text-slate-800 mb-4">
              ⭐ Rate Your Experience
            </h2>
            
            <div className="mb-4">
              <label className="block text-slate-700 font-semibold mb-2">
                Rating
              </label>
              <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    onClick={() => setRating(star)}
                    className={`text-3xl ${
                      star <= rating ? 'text-yellow-400' : 'text-slate-300'
                    }`}
                  >
                    ⭐
                  </button>
                ))}
              </div>
            </div>
            
            <div className="mb-4">
              <label className="block text-slate-700 font-semibold mb-2">
                Comment
              </label>
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                className="w-full border-2 border-slate-300 rounded-lg p-3 focus:border-teal-500 focus:outline-none"
                rows={4}
                placeholder="Share your experience..."
              />
            </div>
            
            <button
              onClick={submitFeedback}
              className="w-full bg-teal-600 text-white py-3 rounded-lg font-bold hover:bg-teal-700"
            >
              Submit Feedback
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
