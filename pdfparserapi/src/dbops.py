import logging
import mysql.connector


class DBOps(object):
    def __init__(self, config, setup=False):
        self.logger = logging.getLogger('CCAI.DbOps')
        self.config = config
        if setup:
            self.setup_db()
        self.create_connection(db_name=True)
        

    def create_connection(self, db_name=False):
        if db_name:
            self.cnx =  mysql.connector.connect(
                        host =self.config['db_host'],
                        port =self.config['db_port'],
                        user =self.config['db_user'],
                        password =self.config['db_password'],
                        database=self.config['db_db_name'],
                    )
        else:
            self.cnx =  mysql.connector.connect(
                        host =self.config['db_host'],
                        port =self.config['db_port'],
                        user =self.config['db_user'],
                        password =self.config['db_password'],
                    )
        self.cursor = self.cnx.cursor(prepared=True)

    def setup_db(self):
        self.logger.info("Setting up db")
        self.create_connection()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS {} ;".format(self.config['db_db_name']))
        self.cnx.commit()
        self.cnx.close()

        self.create_connection(db_name=True)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS claim_meta \
                            (claim_number VARCHAR(64), \
                            company VARCHAR(64), \
                            type_of_loss VARCHAR(64), \
                            insured VARCHAR(64), \
                            estimate VARCHAR(64), \
                            estimator VARCHAR(64), \
                            email VARCHAR(64), \
                            phone VARCHAR(64))")
        self.cnx.commit()
        self.cnx.close()

    def insert_record(self, data):
        try:
            sql_insert_query = "INSERT INTO claim_meta \
                (claim_number, company, type_of_loss, insured, estimate, estimator, email, phone) \
                VALUES ('{claim_number}', '{company}', '{type_of_loss}', '{insured}', '{estimate}', '{estimator}', '{email}', '{phone}')"
            self.cursor.execute(sql_insert_query.format(**data))
            self.cnx.commit()
            self.logger.debug("Data inserted successfully into employee table using the prepared statement")
        except mysql.connector.Error as error:
            self.logger.critical("parameterized query failed {}".format(error))
        
        
        