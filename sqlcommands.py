create_table_categories = 'create table if not exists public.categories (category_id serial primary key, name_category varchar(255))'

insertion_data_categoty = "insert into public.categories (name_category) values('Apple iPhone', 'Apple iPad', 'Apple AirPods', 'accessories', 'for home')"

create_table_goods = 'create table IF NOT EXISTS public.Goods (good_id serial primary key, title varchar(255) unique, price int, old_price int null, category_id int,link_product varchar(255), img_link varchar(255), foreign key (category_id) references categories (category_id))'

select_all_query = "select * from goods order by title;"

select_apple13 = "select * from goods where title like 'Apple iPhone 13 128%' order by title"

select_min_13_price = "select * from goods where title like 'Apple iPhone 13 128%' and price = (select min(price) from goods where title like 'Apple iPhone 13 128%') order by title"

select_max_difference = "select title, price, old_price, (old_price - price) as difference from goods where (old_price - price) = (select max(old_price - price) from goods)"

insert_categories = 'insert into categories (name, description, parent_category) values '
