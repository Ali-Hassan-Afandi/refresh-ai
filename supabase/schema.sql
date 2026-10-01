create extension if not exists "pgcrypto";
create table if not exists negotiations (
 id text primary key, status text not null, round integer not null default 0,
 max_rounds integer not null default 6, seller_data jsonb not null,
 buyer_data jsonb not null, agreed_price numeric, agreed_quantity numeric,
 offers jsonb not null default '[]'::jsonb, events jsonb not null default '[]'::jsonb,
 created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create table if not exists transactions (
 id uuid primary key default gen_random_uuid(),
 negotiation_id text unique references negotiations(id) on delete cascade,
 product text not null, quantity_kg numeric not null, price_per_kg numeric not null,
 total_value numeric not null, seller_business text not null, buyer_business text not null,
 status text not null default 'COMPLETED', created_at timestamptz not null default now()
);
create index if not exists idx_negotiations_status on negotiations(status);
