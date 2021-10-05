-- upgrade --
ALTER TABLE "reservations" DROP COLUMN "grand_total";
-- downgrade --
ALTER TABLE "reservations" ADD "grand_total" DECIMAL(10,2) NOT NULL;
