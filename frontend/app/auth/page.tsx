'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { authAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

export default function AuthPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { login } = useAuthStore();

  const [isLogin, setIsLogin] = useState(true);
  const [role, setRole] = useState('patient');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    full_name: '',
    phone_number: '',
    email: '',
    password: '',
  });

  useEffect(() => {
    const roleParam = searchParams.get('role');
    if (roleParam) {
      setRole(roleParam);
    }
  }, [searchParams]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        // Login
        const response = await authAPI.login({
          phone_number: formData.phone_number,
          password: formData.password,
        });

        login(response.access_token, {
          user_id: response.user_id,
          role: response.role,
          full_name: response.full_name,
        });

        // Redirect based on role
        if (response.role === 'system_owner') {
          router.push('/owner/dashboard');
        } else if (response.role === 'patient') {
          router.push('/patient/dashboard');
        } else {
          router.push('/dashboard');
        }
      } else {
        // Signup
        const response = await authAPI.signup({
          ...formData,
          role,
        });

        login(response.access_token, {
          user_id: response.user_id,
          role: response.role,
          full_name: response.full_name,
        });

        // Redirect based on role
        if (response.role === 'system_owner') {
          router.push('/owner/dashboard');
        } else if (response.role === 'patient') {
          router.push('/patient/dashboard');
        } else {
          router.push('/dashboard');
        }
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const roleLabels: Record<string, string> = {
    patient: 'Patient',
    nurse_provider: 'Nurse Provider',
    dispenser_provider: 'Dispenser Provider',
    hospital_admin: 'Hospital Admin',
    pharmacy_admin: 'Pharmacy Admin',
    system_owner: 'System Owner',
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 to-blue-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-teal-800 mb-2">
            E-SHIFA AI PORTAL
          </h1>
          <p className="text-slate-600">
            {isLogin ? 'Sign In' : 'Create Account'} as {roleLabels[role]}
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-2">
                Full Name
              </label>
              <input
                type="text"
                required
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                placeholder="M. Suhail Shaikh"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-bold text-slate-700 mb-2">
              Phone Number
            </label>
            <input
              type="tel"
              required
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              placeholder="+923001234567"
              value={formData.phone_number}
              onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
            />
          </div>

          {!isLogin && (
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-2">
                Email (Optional)
              </label>
              <input
                type="email"
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                placeholder="suhail@eshifa.ai"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-bold text-slate-700 mb-2">
              Password
            </label>
            <input
              type="password"
              required
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              placeholder="••••••••"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            />
          </div>

          {!isLogin && (
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-2">
                Role
              </label>
              <select
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              >
                <option value="patient">Patient</option>
                <option value="nurse_provider">Nurse Provider</option>
                <option value="dispenser_provider">Dispenser Provider</option>
                <option value="hospital_admin">Hospital Admin</option>
                <option value="pharmacy_admin">Pharmacy Admin</option>
                <option value="system_owner">System Owner</option>
              </select>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-teal-600 text-white py-3 rounded-lg font-bold hover:bg-teal-700 transition-colors disabled:bg-slate-400"
          >
            {loading ? 'Processing...' : isLogin ? 'SECURE SIGN IN' : 'REGISTER ACCOUNT'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <button
            onClick={() => setIsLogin(!isLogin)}
            className="text-teal-600 hover:text-teal-800 font-semibold"
          >
            {isLogin ? "Don't have an account? Register" : 'Already have an account? Sign In'}
          </button>
        </div>

        <div className="mt-6 text-center">
          <button
            onClick={() => router.push('/')}
            className="text-slate-500 hover:text-slate-700 text-sm"
          >
            ← Back to Home
          </button>
        </div>
      </div>
    </div>
  );
}
