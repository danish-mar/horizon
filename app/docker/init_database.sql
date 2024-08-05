create database if not exists nebula;

use nebula;

create table User
(
    user_id       int auto_increment
        primary key,
    username      varchar(50)                        not null,
    password_hash varchar(255)                       not null,
    first_name    varchar(50)                        not null,
    last_name     varchar(50)                        not null,
    email         varchar(100)                       not null,
    phone_number  varchar(20)                        null,
    created_at    datetime default CURRENT_TIMESTAMP null,
    last_login    datetime default CURRENT_TIMESTAMP null,
    constraint email
        unique (email),
    constraint username
        unique (username)
);

create table Account
(
    account_id     int auto_increment
        primary key,
    user_id        int                                  not null,
    account_number varchar(20)                          not null,
    account_type   enum ('savings', 'current', 'other') not null,
    balance        decimal(10, 2)                       not null,
    created_at     datetime default CURRENT_TIMESTAMP   null,
    constraint account_number
        unique (account_number),
    constraint Account_ibfk_1
        foreign key (user_id) references User (user_id)
);

create index user_id
    on Account (user_id);

create table Auth_Key
(
    auth_key         varchar(255) not null
        primary key,
    user_id          int          not null,
    expiry_timestamp datetime     not null,
    constraint Auth_Key_ibfk_1
        foreign key (user_id) references User (user_id)
);

create index user_id
    on Auth_Key (user_id);

create table Transaction
(
    transaction_id   int auto_increment
        primary key,
    account_id       int                                      not null,
    amount           decimal(10, 2)                           not null,
    transaction_type enum ('debit', 'credit')                 not null,
    description      varchar(255)                             null,
    created_at       datetime default CURRENT_TIMESTAMP       null,
    previous_hash    varchar(255)                             not null,
    from_account     varchar(20)                              null,
    to_account       varchar(20)                              null,
    platform         enum ('Internet Banking', 'NPI', 'Card') not null,
    constraint Transaction_ibfk_1
        foreign key (account_id) references Account (account_id),
    constraint fk_from_account
        foreign key (from_account) references Account (account_number),
    constraint fk_to_account
        foreign key (to_account) references Account (account_number)
);

create index account_id
    on Transaction (account_id);


