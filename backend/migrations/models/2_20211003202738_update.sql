-- upgrade --
ALTER TABLE "reservations" ADD "capacity" INT NOT NULL  DEFAULT 0;
ALTER TABLE "reservations" DROP COLUMN "kid_price";
ALTER TABLE "reservations" DROP COLUMN "adult_price";
-- downgrade --
ALTER TABLE "reservations" ADD "kid_price" DECIMAL(10,2) NOT NULL  DEFAULT 4000;
ALTER TABLE "reservations" ADD "adult_price" DECIMAL(10,2) NOT NULL  DEFAULT 7500;
ALTER TABLE "reservations" DROP COLUMN "capacity";
