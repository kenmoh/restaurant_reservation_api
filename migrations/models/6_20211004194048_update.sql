-- upgrade --
ALTER TABLE "reservations" DROP COLUMN "capacity";
-- downgrade --
ALTER TABLE "reservations" ADD "capacity" INT NOT NULL  DEFAULT 5;
