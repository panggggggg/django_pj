CREATE TABLE "users" (
  "user_id" integer PRIMARY KEY,
  "first_name" varchar,
  "last_name" varchar,
  "username" varchar,
  "password" integer,
  "age" integer,
  "role" integer,
  "image" varchar
);

CREATE TABLE "posts" (
  "post_id" integer PRIMARY KEY,
  "user_id" integer,
  "title" varchar,
  "body" varchar,
  "created_at" datetime,
  "active" integer,
  "image" varchar
);

CREATE TABLE "shares" (
  "share_id" integer PRIMARY KEY,
  "post_id" integer,
  "count" integer,
  "user_id" integer
);

CREATE TABLE "category" (
  "category_id" integer PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "post_Category" (
  "category_id" integer,
  "post_id" integer
);

CREATE TABLE "comment" (
  "comment_id" integer PRIMARY KEY,
  "user_id" integer,
  "comment" varchar,
  "post_id" integer,
  "created_at" datetime
);

ALTER TABLE "users" ADD FOREIGN KEY ("user_id") REFERENCES "posts" ("user_id");

CREATE TABLE "users_shares" (
  "users_user_id" integer,
  "shares_user_id" integer,
  PRIMARY KEY ("users_user_id", "shares_user_id")
);

ALTER TABLE "users_shares" ADD FOREIGN KEY ("users_user_id") REFERENCES "users" ("user_id");

ALTER TABLE "users_shares" ADD FOREIGN KEY ("shares_user_id") REFERENCES "shares" ("user_id");


ALTER TABLE "shares" ADD FOREIGN KEY ("post_id") REFERENCES "posts" ("post_id");

ALTER TABLE "post_Category" ADD FOREIGN KEY ("category_id") REFERENCES "category" ("category_id");

ALTER TABLE "post_Category" ADD FOREIGN KEY ("post_id") REFERENCES "posts" ("post_id");

CREATE TABLE "comment_users" (
  "comment_user_id" integer,
  "users_user_id" integer,
  PRIMARY KEY ("comment_user_id", "users_user_id")
);

ALTER TABLE "comment_users" ADD FOREIGN KEY ("comment_user_id") REFERENCES "comment" ("user_id");

ALTER TABLE "comment_users" ADD FOREIGN KEY ("users_user_id") REFERENCES "users" ("user_id");


CREATE TABLE "comment_posts" (
  "comment_post_id" integer,
  "posts_post_id" integer,
  PRIMARY KEY ("comment_post_id", "posts_post_id")
);

ALTER TABLE "comment_posts" ADD FOREIGN KEY ("comment_post_id") REFERENCES "comment" ("post_id");

ALTER TABLE "comment_posts" ADD FOREIGN KEY ("posts_post_id") REFERENCES "posts" ("post_id");

