
table1 = """
        CREATE TABLE IF NOT EXISTS users (
        user_id serial PRIMARY KEY,
        first_name varchar (40) NOT NULL,
        last_name varchar (40) NOT NULL,
        othername varchar (40),
        email varchar(40) UNIQUE NOT NULL,
        user_name varchar  (40) UNIQUE NOT NULL,
        password varchar(60) NOT NULL,
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
        topic varchar(40) UNIQUE NOT NULL,
        happeningon timestamp  NOT NULL,
        tags VARCHAR(20) ARRAY,
        name varchar(20) NOT NULL,
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

tables = [table1,table2,table3,table4,table5]
