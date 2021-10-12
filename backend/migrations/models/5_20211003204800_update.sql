-- upgrade --
ALTER TABLE "reservations" ALTER COLUMN "capacity" SET DEFAULT 5;
-- downgrade --
ALTER TABLE "reservations" ALTER COLUMN "capacity" SET DEFAULT 1000;
