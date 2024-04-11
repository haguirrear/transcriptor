create table
  public.profiles (
    id uuid not null,
    created_at timestamp with time zone null default now(),
    updated_at timestamp with time zone null,
    full_name character varying null,
    avatar_url character varying null,
    constraint profiles_pkey primary key (id),
    constraint profiles_id_fkey foreign key (id) references auth.users (id) on update cascade on delete cascade
  ) tablespace pg_default;
