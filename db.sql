drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  t1 integer not null,
  t2 integer not null,
  t3 integer,
  title string not null,
  abstract string not null,
  date_time sting not null,
  body string not null
);