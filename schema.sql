drop table if exists secrets;
create table secrets (
    id integer primary key autoincrement,
    name varchar not null,
    head integer,
    foreign key (head) references messages(id)
);

drop table if exists messages;
create table messages (
    id integer primary key autoincrement,
    has_note boolean not null,
    filename varchar,
    prev integer,
    foreign key (prev) references messages(id)
);
