-- upgrade --
ALTER TABLE "reservations" ALTER COLUMN "number_of_seat_children" SET DEFAULT 0;
ALTER TABLE "reservations" ALTER COLUMN "number_of_seat_children" TYPE INT USING "number_of_seat_children"::INT;
ALTER TABLE "reservations" ALTER COLUMN "number_of_seat_adults" SET DEFAULT 0;
ALTER TABLE "reservations" ALTER COLUMN "number_of_seat_adults" TYPE INT USING "number_of_seat_adults"::INT;
ALTER TABLE "reservations" ALTER COLUMN "kid_price" TYPE DECIMAL(10,2) USING "kid_price"::DECIMAL(10,2);
ALTER TABLE "reservations" ALTER COLUMN "adult_price" TYPE DECIMAL(10,2) USING "adult_price"::DECIMAL(10,2);
ALTER TABLE "reservations" ALTER COLUMN "additional_info" DROP NOT NULL;
-- downgrade --
ALTER TABLE "reservations" ALTER COLUMN "number_of_seat_children" SET DEFAULT 1;
ALTER TABLE "reservations" ALTER COLUMN "number_of_seat_children" TYPE INT USING "number_of_seat_children"::INT;
ALTER TABLE "reservations" ALTER COLUMN "number_of_seat_adults" SET DEFAULT 1;
ALTER TABLE "reservations" ALTER COLUMN "number_of_seat_adults" TYPE INT USING "number_of_seat_adults"::INT;
ALTER TABLE "reservations" ALTER COLUMN "kid_price" TYPE DECIMAL(10,2) USING "kid_price"::DECIMAL(10,2);
ALTER TABLE "reservations" ALTER COLUMN "adult_price" TYPE DECIMAL(10,2) USING "adult_price"::DECIMAL(10,2);
ALTER TABLE "reservations" ALTER COLUMN "additional_info" SET NOT NULL;
