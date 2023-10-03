ALTER TABLE users
ADD COLUMN payment_status TEXT NOT NULL DEFAULT 'onboarding',
ADD COLUMN start_trial_at TIMESTAMPTZ,
ADD COLUMN last_paid_at TIMESTAMPTZ;
