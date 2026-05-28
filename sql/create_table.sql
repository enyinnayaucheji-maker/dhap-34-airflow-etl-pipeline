CREATE TABLE IF NOT EXISTS public.email_support_dataset (

    subject TEXT NOT NULL,
    sender TEXT NOT NULL,
    receiver TEXT NOT NULL,

    timestamp TIMESTAMP NOT NULL,

    message_body TEXT NOT NULL,

    thread_id TEXT NOT NULL,

    email_types TEXT NOT NULL,

    email_status TEXT NOT NULL,

    email_criticality TEXT NOT NULL,

    product_types TEXT NOT NULL,

    agent_effectivity TEXT NOT NULL,

    agent_efficiency TEXT NOT NULL,

    customer_satisfaction FLOAT NOT NULL
);