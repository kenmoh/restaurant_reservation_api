-- upgrade --
CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL  DEFAULT 'Mrs',
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "full_name" VARCHAR(255) NOT NULL,
    "phone" VARCHAR(255) NOT NULL UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "is_admin" BOOL NOT NULL  DEFAULT False,
    "is_staff" BOOL NOT NULL  DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "users"."is_admin" IS 'Manager';
COMMENT ON COLUMN "users"."is_staff" IS 'Supervisor';
CREATE TABLE IF NOT EXISTS "reservations" (
    "booking_id" UUID NOT NULL  PRIMARY KEY,
    "number_of_seat_adults" INT NOT NULL  DEFAULT 1,
    "number_of_seat_children" INT NOT NULL  DEFAULT 1,
    "kid_price" DECIMAL(10,2) NOT NULL  DEFAULT 4000,
    "adult_price" DECIMAL(10,2) NOT NULL  DEFAULT 7500,
    "serving_period" VARCHAR(255) NOT NULL  DEFAULT 'Breakfast',
    "deposit" BOOL NOT NULL  DEFAULT False,
    "additional_info" TEXT NOT NULL,
    "is_complete" BOOL NOT NULL  DEFAULT False,
    "cancel_reservation" BOOL NOT NULL  DEFAULT False,
    "date_booked" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "arrival_date" VARCHAR(255) NOT NULL,
    "grand_total" DECIMAL(10,2) NOT NULL,
    "user_id" VARCHAR(255) NOT NULL REFERENCES "users" ("username") ON DELETE CASCADE
);
COMMENT ON COLUMN "reservations"."number_of_seat_adults" IS 'Age 14 and Above';
COMMENT ON COLUMN "reservations"."number_of_seat_children" IS 'Age 7 - 13';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
