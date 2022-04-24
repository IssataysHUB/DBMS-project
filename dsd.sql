

CREATE TABLE user_addresses (
  user_id int, 
  street varchar(30) NOT NULL,
  city_id int NOT NULL,
  state_id int NOT NULL,
  PRIMARY KEY (user_id),
  FOREIGN KEY (user_id)
      REFERENCES auth_user (id)
      ON DELETE CASCADE,
  FOREIGN KEY (city_id)
      REFERENCES cities (id)
      ON DELETE CASCADE,
  FOREIGN KEY (state_id)
      REFERENCES states (id)
      ON DELETE CASCADE
);

CREATE TABLE goods (
  id integer,
  title varchar(100) NOT NULL,
  seller varchar(100) NOT NULL,
  published_date timestamp NOT NULL,
  code char(12),
  price int,
  PRIMARY KEY (id),
  UNIQUE (code)
);

select * from goods;

CREATE TABLE reviews (
  id integer,
  good_id integer NOT NULL,
  reviewer_name varchar(255),
  content varchar(255),
  published_date timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (good_id)
      REFERENCES goods(id)
      ON DELETE CASCADE
);

CREATE TABLE user_checkouts (
  id integer,
  user_id int NOT NULL,
  good_id int NOT NULL,
  checkout_date timestamp,
  return_date timestamp,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES auth_user(id)
                        ON DELETE CASCADE,
  FOREIGN KEY (good_id) REFERENCES goods(id)
                        ON DELETE CASCADE
);

        
INSERT INTO user_checkouts VALUES (3, 2, 2, CURRENT_TIMESTAMP, null);
INSERT INTO user_checkouts VALUES (4, 2, 3, CURRENT_TIMESTAMP, null);
INSERT INTO user_checkouts VALUES (5, 2, 5, CURRENT_TIMESTAMP, null);


INSERT INTO cities
  VALUES
         (3, 'Oral', 1);


CREATE TABLE cities (
  id int,
  city_name varchar(255) NOT NULL,
  state_id integer NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (state_id) REFERENCES states(id)
                        ON DELETE CASCADE
);


INSERT INTO cities
  VALUES
         (1, 'Oral', 3);

INSERT INTO cities
  VALUES
         (2, 'Shalkar', 2);

CREATE TABLE states (
  id int,
  state_name varchar(255) NOT NULL,
  postal_code varchar(255) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO states
  VALUES
         (3, 'Oral', '1224');
         
         
         
--INSERT_ALL_GOODS PROCEDURE
CREATE OR REPLACE PROCEDURE insert_all_goods (
    title VARCHAR2,
    seller VARCHAR2,
    date DATE,
    code VARCHAR2,
    price NUMBER
    ) IS
BEGIN
    INSERT INTO books (
        Title,
        Seller,
        published_date,
        code,
        Price)
    VALUES (
        title,
        seller,
        date,
        cpde,
        price
        );
END;


--DELETE_GOOD PROCEDURE
CREATE OR REPLACE PROCEDURE delete_good(p_id INTEGER) IS
BEGIN
    DELETE FROM goods WHERE ID = p_id;
    DBMS_OUTPUT.PUT_LINE('Deleted successfully');
END;



---UPDATE_GOOD PROCEDURE
CREATE OR REPLACE PROCEDURE update_good(
    u_id NUMBER,
    u_title VARCHAR2,
    u_seller VARCHAR2,
    u_code VARCHAR2,
    u_price NUMBER
) IS
BEGIN
    UPDATE books
    SET title  = u_title,
    seller = u_seller,
    code = u_code,
    price = u_price

    WHERE id = u_id;
END;


SET SERVEROUTPUT ON;
--age_converter FUNCTION
CREATE OR REPLACE FUNCTION date_converter(p_date Date)
RETURN NUMBER
IS
v_age Number;
BEGIN
    v_age := EXTRACT(YEAR FROM SYSDATE) - EXTRACT(YEAR FROM p_date);
    RETURN v_age;
END;
---EXAMPLE
SELECT ID, date_converter(published_date) FROM books;

CREATE OR REPLACE FUNCTION price_converter(Price NUMBER, currency_in_tg NUMBER)
RETURN NUMBER
IS
price_in_tg NUMBER;
BEGIN
    price_in_tg := Price  * currency_in_tg;
    RETURN price_in_tg;
END;
drop procedure sort_by_column;



SELECT user_checkouts.id, auth_user.username, goods.title, user_checkouts.checkout_date
FROM user_checkouts
LEFT JOIN goods ON user_checkouts.good_id = goods.id
INNER JOIN auth_user ON user_checkouts.user_id=auth_user.id;