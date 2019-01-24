
table1 = """
        CREATE TABLE IF NOT EXISTS users (
        user_id serial PRIMARY KEY,
        first_name varchar (40) NOT NULL,
        last_name varchar (40) NOT NULL,
        othername varchar (40),
        email varchar(40) UNIQUE NOT NULL,
        user_name varchar  (40) UNIQUE NOT NULL,
        password varchar(200) NOT NULL,
        isAdmin bool DEFAULT False,
        registered timestamp
        )
        """
table2="""
        CREATE TABLE IF NOT EXISTS meetups(
        meetup_id serial PRIMARY KEY,
        createdon timestamp  NOT NULL,
        location varchar(40) NOT NULL,
        images varchar(40) ARRAY ,
        topic varchar(40) UNIQUE  NOT NULL,
        happeningon timestamp  NOT NULL,
        tags VARCHAR(20) ARRAY,
        name varchar(20)  NOT NULL,
        createdby INT NOT NULL
        )
        """

table3= """
        CREATE TABLE IF NOT EXISTS questions(
        question_id serial PRIMARY KEY,
        createdon timestamp  NOT NULL,
        createdby INT NOT NULL,
        meetup INT NOT NULL,
        title varchar(40) UNIQUE NOT NULL,
        body VARCHAR(40) NOT NULL,
        votes INT DEFAULT 0
        )
        """

table4= """
        CREATE TABLE IF NOT EXISTS Rsvp(
        rsvp_id serial PRIMARY KEY,
        meetup INT  NOT NULL,
        user_ INT NOT NULL,
        response VARCHAR(40) NOt NULL
        
        )
        """

table5= """
        CREATE TABLE IF NOT EXISTS comments(
        comment_id serial PRIMARY KEY,
        createdon timestamp  NOT NULL,
        createdby INT REFERENCES users(user_id),
        meetup INT ,
        title varchar(40) UNIQUE NOT NULL,
        body VARCHAR(60) NOT NULL,
        question INT NOT NULL
        
        )
        """
save_user =     """
                INSERT INTO users (first_name, last_name, othername, email,
                                                user_name, password, isadmin, registered)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING user_id, user_name, email, password
                """

save_question = """
                INSERT INTO questions (title, body, meetup)
                VALUES(%s,%s,%s) RETURNING question_id, title, body
                """
save_comment = """
                INSERT INTO comments (createdon,createdby,meetup,title,body,question),
                VALUES(%s,%s,%s,%s,%s,%s) RETURNING comment_id, meetup, title, body, question
                """
create_meetup = """
                INSERT INTO meetups (createdon, location,images,topic,
                happeningon,tags,name,createdby)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING meetup_id, name, happeningon
                """
create_rsvp = """
                INSERT INTO rsvp (meetup,user_,response),
                VALUES(%s,%s,%s) RETURNING meetup_id, response
              """
check_same_meetup_name = """
                          SELECT name FROM meetups WHERE topic = %s
                          """
get_a_user_email = """
                        SELECT email from users WHERE email =%s
                        
                   """
get_a_user_by_username= """
                            SELECT user_name,user_id from users WHERE user_name = %s
                        """
geta_user_by_username= """
                            SELECT * from users WHERE user_name = %s
                        """
                        
get_user_by_id = """
                    SELECT * FROM users WHERE user_name = %s;
                 """

get_question_by_id= """
                        SELECT question_id FROM questions WHERE question_id = %s;
                    """

get_meetup_by_id = """
                        SELECT * FROM meetups WHERE meetup_id = %s
                   """
                
delet_meetup_by_id = """
                        DELETE meetup_id FROM meetups WHERE meetup_id = %s;
                     """

get_upcoming_meetups = """
                        SELECT * FROM meetups WHERE happeningon > %s
                       """

update_votes = """
                UPDATE questions SET votes = %s WHERE votes = 0;
               """
drop_table = """DROP TABLE users IF exist"""




tables = [table1,table2,table3,table4,table5]
