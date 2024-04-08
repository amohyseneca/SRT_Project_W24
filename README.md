# SRTProject
## Project Setup:
### Packages:
```pip3 install flask```
```pip3 install mysql.connector```

### Database Setup:
```
CREATE TABLE {DATABASE NAME}.`reviews` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200) NOT NULL,
  `rating` INT NOT NULL,
  `author` VARCHAR(100) NOT NULL,
  `genre` VARCHAR(200) NOT NULL,
  `pubdate` DATE NOT NULL,
  `review` TEXT(16383) NOT NULL,
  `imdbid` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`)
);
```

```
CREATE TABLE {DATABASE NAME}.`comments` (
    `comment_id` INT NOT NULL AUTO_INCREMENT,
    `comment_text` TEXT(1000) NOT NULL,
    `review_id` INT NOT NULL,
    `comment_date` DATE NOT NULL,
    FOREIGN KEY (`review_id`) REFERENCES reviews(`id`),
    PRIMARY KEY (`comment_id`)
);
```
