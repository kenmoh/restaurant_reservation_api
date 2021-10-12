-- upgrade --
ALTER TABLE "reservations" RENAME COLUMN "booking_id" TO "reservation_id";
ALTER TABLE "reservations" ADD "date_modified" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
-- downgrade --
ALTER TABLE "reservations" RENAME COLUMN "reservation_id" TO "booking_id";
ALTER TABLE "reservations" DROP COLUMN "date_modified";
