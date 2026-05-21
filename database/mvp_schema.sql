-- E-Shifa AI - Hackathon MVP Schema
-- AI-Powered Home Healthcare Service Orchestrator

DROP TABLE IF EXISTS disputes CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS ai_traces CASCADE;
DROP TABLE IF EXISTS bookings CASCADE;
DROP TABLE IF EXISTS providers CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS users_auth CASCADE;

-- Users Auth (Authentication table)
CREATE TABLE users_auth (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) CHECK (role IN ('customer', 'provider', 'admin')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users (Extended profile)
CREATE TABLE users (
    id UUID PRIMARY KEY REFERENCES users_auth(id) ON DELETE CASCADE,
    loyalty_tier VARCHAR(20) DEFAULT 'bronze',
    total_bookings INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Providers
CREATE TABLE providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users_auth(id) ON DELETE CASCADE,
    service_type VARCHAR(50) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    base_rate DECIMAL(10, 2) NOT NULL,
    rating DECIMAL(3, 2) DEFAULT 5.0,
    total_bookings INT DEFAULT 0,
    cancellation_rate DECIMAL(5, 4) DEFAULT 0.0,
    is_available BOOLEAN DEFAULT true,
    specialization TEXT[],
    response_time_avg_minutes INT DEFAULT 15,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bookings
CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_number VARCHAR(20) UNIQUE,
    customer_id UUID REFERENCES users_auth(id),
    provider_id UUID REFERENCES providers(id),
    service_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    urgency VARCHAR(20) DEFAULT 'routine',
    scheduled_time TIMESTAMP NOT NULL,
    customer_location JSONB NOT NULL,
    distance_km DECIMAL(6, 2),
    base_price DECIMAL(10, 2),
    distance_fee DECIMAL(10, 2),
    urgency_surcharge DECIMAL(10, 2),
    demand_surge DECIMAL(10, 2),
    loyalty_discount DECIMAL(10, 2),
    final_price DECIMAL(10, 2),
    user_query TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI Traces
CREATE TABLE ai_traces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID REFERENCES bookings(id),
    agent_name VARCHAR(50) NOT NULL,
    input_data JSONB NOT NULL,
    reasoning_steps JSONB NOT NULL,
    output_data JSONB NOT NULL,
    execution_time_ms INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews
CREATE TABLE reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID REFERENCES bookings(id),
    customer_id UUID REFERENCES users_auth(id),
    provider_id UUID REFERENCES providers(id),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    sentiment_score DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notifications
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users_auth(id),
    booking_id UUID REFERENCES bookings(id),
    type VARCHAR(50),
    channel VARCHAR(20),
    message TEXT,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Disputes
CREATE TABLE disputes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID REFERENCES bookings(id),
    raised_by UUID REFERENCES users_auth(id),
    reason TEXT,
    status VARCHAR(20) DEFAULT 'open',
    resolution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample Data
INSERT INTO users_auth (phone_number, full_name, password_hash, role, email) VALUES
('+923001234567', 'Ahmed Khan', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Vu', 'customer', 'ahmed@example.com'),
('+923009876543', 'Fatima Bibi', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Vu', 'provider', 'fatima@example.com'),
('+923007654321', 'Dr. Ali Raza', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Vu', 'provider', 'ali@example.com'),
('+923005555555', 'Admin User', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Vu', 'admin', 'admin@example.com');

INSERT INTO users (id, loyalty_tier) VALUES
((SELECT id FROM users_auth WHERE phone_number = '+923001234567'), 'silver');

INSERT INTO providers (user_id, service_type, latitude, longitude, base_rate, rating, specialization) VALUES
((SELECT id FROM users_auth WHERE phone_number = '+923009876543'), 'home_nurse', 24.8607, 67.0011, 1500, 4.8, ARRAY['general_nursing', 'elderly_care']),
((SELECT id FROM users_auth WHERE phone_number = '+923007654321'), 'doctor_visit', 24.8700, 67.0100, 3000, 4.9, ARRAY['general_physician', 'emergency']);
