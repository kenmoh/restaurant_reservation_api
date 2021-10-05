-- upgrade --
ALTER TABLE "reservations" ALTER COLUMN "capacity" SET DEFAULT 1000;
-- downgrade --
ALTER TABLE "reservations" ALTER COLUMN "capacity" SET DEFAULT 0;
