DROP DATABASE IF EXISTS test;
CREATE DATABASE test;

\c test

CREATE EXTENSION postgis;

DROP TABLE IF EXISTS favourite_products;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS price_report;
DROP TABLE IF EXISTS stores;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;


CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category VARCHAR(255) NOT NULL
);


CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product VARCHAR(255) NOT NULL,
    description TEXT,
    brand VARCHAR(255),
    size VARCHAR(50),
    category_id INT NOT NULL,
    product_photo_url TEXT,
    FOREIGN KEY (category_id) REFERENCES categories (category_id)
);



CREATE TABLE stores (
    store_id SERIAL PRIMARY KEY,
    store_name VARCHAR(255) NOT NULL,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL
);


CREATE TABLE price_report (
    price_id SERIAL PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,
    store_id INT NOT NULL,
    product_id INT NOT NULL,
    submission_time TIMESTAMP NOT NULL,
    product_photo_url TEXT,
    FOREIGN KEY (store_id) REFERENCES Stores (store_id),
    FOREIGN KEY (product_id) REFERENCES Products (product_id)
);


CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    avatar_url TEXT
);


CREATE TABLE favourite_products (
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    product_name VARCHAR(255),
    PRIMARY KEY (user_id, product_id),
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    FOREIGN KEY (product_id) REFERENCES Products (product_id)
);

INSERT INTO categories (category) VALUES
('Fruits'),
('Vegetables'),
('Dairy'),
('Beverages'),
('Snacks');
INSERT INTO products (product, description, brand, size, category_id, product_photo_url) VALUES
('Apple', 'Fresh red apples', 'FreshFarms', '1kg', 1, 'http://example.com/apple.jpg'),
('Banana', 'Organic bananas', 'GreenEarth', '1kg', 1, 'http://example.com/banana.jpg'),
('Carrot', 'Crunchy carrots', 'VeggieDelight', '1kg', 2, 'http://example.com/carrot.jpg'),
('Broccoli', 'Fresh broccoli', 'VeggieDelight', '500g', 2, 'http://example.com/broccoli.jpg'),
('Milk', 'Whole milk', 'DairyPure', '1L', 3, 'http://example.com/milk.jpg'),
('Cheese', 'Cheddar cheese', 'DairyPure', '200g', 3, 'http://example.com/cheese.jpg'),
('Orange Juice', 'Fresh orange juice', 'JuiceWorld', '1L', 4, 'http://example.com/oj.jpg'),
('Cola', 'Soft drink', 'ColaCo', '1.5L', 4, 'http://example.com/cola.jpg'),
('Chips', 'Potato chips', 'Snacky', '200g', 5, 'http://example.com/chips.jpg'),
('Cookies', 'Chocolate chip cookies', 'Snacky', '300g', 5, 'http://example.com/cookies.jpg');
INSERT INTO stores (store_name, latitude, longitude) VALUES
('SuperMart', 51.5074, -0.1278),   -- London
('GroceryLand', 53.4808, -2.2426), -- Manchester
('FreshMarket', 52.4862, -1.8904), -- Birmingham
('HealthyFoods', 53.4084, -2.9916),-- Liverpool
('BudgetGroceries', 53.8008, -1.5491),-- Leeds
('QuickShop', 53.3811, -1.4701),   -- Sheffield
('GreenGrocer', 51.4545, -2.5879), -- Bristol
('OrganicMarket', 54.9784, -1.6174),-- Newcastle
('FoodBarn', 52.9548, -1.1581),    -- Nottingham
('FarmFresh', 50.9097, -1.4044),   -- Southampton
('DiscountGroceries', 51.7520, -1.2577),-- Oxford
('NeighborhoodMarket', 52.2053, 0.1218),-- Cambridge
('CityMarket', 50.8225, -0.1372),  -- Brighton
('TownGrocer', 53.9590, -1.0815),  -- York
('VillageMarket', 51.3758, -2.3599);-- Bath
INSERT INTO users (username, password, email, avatar_url) VALUES
('john_doe', 'password123', 'john@example.com', 'http://example.com/john.jpg'),
('jane_smith', 'password123', 'jane@example.com', 'http://example.com/jane.jpg'),
('sam_jones', 'password123', 'sam@example.com', 'http://example.com/sam.jpg'),
('lisa_white', 'password123', 'lisa@example.com', 'http://example.com/lisa.jpg'),
('mark_brown', 'password123', 'mark@example.com', 'http://example.com/mark.jpg'),
('nina_black', 'password123', 'nina@example.com', 'http://example.com/nina.jpg'),
('paul_green', 'password123', 'paul@example.com', 'http://example.com/paul.jpg'),
('emma_blue', 'password123', 'emma@example.com', 'http://example.com/emma.jpg'),
('oliver_gray', 'password123', 'oliver@example.com', 'http://example.com/oliver.jpg'),
('lucas_yellow', 'password123', 'lucas@example.com', 'http://example.com/lucas.jpg');
INSERT INTO favourite_products (user_id, product_id, product_name) VALUES
(1, 1, 'Apple'),
(1, 5, 'Milk'),
(2, 2, 'Banana'),
(2, 6, 'Cheese'),
(3, 3, 'Carrot'),
(3, 7, 'Orange Juice'),
(4, 4, 'Broccoli'),
(4, 8, 'Cola'),
(5, 5, 'Milk'),
(5, 9, 'Chips'),
(6, 6, 'Cheese'),
(6, 10, 'Cookies'),
(7, 7, 'Orange Juice'),
(7, 1, 'Apple'),
(8, 8, 'Cola'),
(8, 2, 'Banana'),
(9, 9, 'Chips'),
(9, 3, 'Carrot'),
(10, 10, 'Cookies'),
(10, 4, 'Broccoli');
INSERT INTO price_report (price, store_id, product_id, submission_time, product_photo_url) VALUES
(1.99, 1, 1, '2024-06-01 10:00:00', 'http://example.com/apple.jpg'),
(0.99, 2, 2, '2024-06-01 11:00:00', 'http://example.com/banana.jpg'),
(2.49, 3, 3, '2024-06-01 12:00:00', 'http://example.com/carrot.jpg'),
(1.89, 4, 4, '2024-06-01 13:00:00', 'http://example.com/broccoli.jpg'),
(3.99, 5, 5, '2024-06-01 14:00:00', 'http://example.com/milk.jpg'),
(4.99, 6, 6, '2024-06-01 15:00:00', 'http://example.com/cheese.jpg'),
(2.99, 7, 7, '2024-06-01 16:00:00', 'http://example.com/oj.jpg'),
(1.49, 8, 8, '2024-06-01 17:00:00', 'http://example.com/cola.jpg'),
(2.29, 9, 9, '2024-06-01 18:00:00', 'http://example.com/chips.jpg'),
(3.49, 10, 10, '2024-06-01 19:00:00', 'http://example.com/cookies.jpg');
