
from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    @staticmethod
    def get_colors():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT gp.Product_color as c
                        FROM go_products gp 
                        ORDER BY gp.Product_color
                                   """
            cursor.execute(query)

            for row in cursor:
                result.append(row['c'])

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllNodes(colore):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT gp.*
                        FROM go_products gp 
                        WHERE gp.Product_color = %s
                                       """
            cursor.execute(query, (colore,))

            for row in cursor:
                result.append(Product(**row))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllArchi(colore, anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT t.p1 as p1, t.p2 as p2, COUNT(*) as peso
                        FROM (SELECT DISTINCT t1.p1, t2.p2, t1.d1 
                                FROM (SELECT DISTINCT gp.Product_number as p1, gds.Retailer_code as r1, gds.`Date` as d1
                                        FROM go_products gp, go_daily_sales gds  
                                        WHERE gp.Product_color = "White"
                                                and gds.Product_number = gp.Product_number
                                                and year(gds.Date) = 2018) t1, 
                                        (SELECT DISTINCT gp.Product_number as p2, gds.Retailer_code as r2, gds.`Date` as d2
                                        FROM go_products gp, go_daily_sales gds 
                                        WHERE gp.Product_color = "White"
                                                and gds.Product_number = gp.Product_number
                                                and year(gds.Date) = 2018) t2
                                WHERE t1.r1 = t2.r2
                                and t1.d1 = t2.d2
                                and t1.p1 > t2.p2) t
                        GROUP BY t.p1, t.p2

                                           """
            cursor.execute(query, (colore, anno, colore, anno))

            for row in cursor:
                result.append((row['p1'], row['p2'], row['peso']))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllArchi2(anno, colore):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT gp.Product_number as p, gds.Retailer_code as r, gds.`Date` as d
                        FROM go_products gp, go_daily_sales gds 
                        WHERE gp.Product_number = gds.Product_number
                                and gp.Product_color = %s
                                and year(gds.Date) = %s
                                       """
            cursor.execute(query, (colore, anno))

            for row in cursor:
                result.append((row['p'], row['r'], row['d']))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getPeso(n1, n2, anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT COUNT(DISTINCT gds1.`Date`) as peso
                        FROM go_daily_sales gds1, go_daily_sales gds2
                        WHERE gds1.Product_number = %s
                                and gds2.Product_number = %s
                                and gds1.`Date` = gds2.`Date`
                                and year(gds1.Date) = %s
                                and gds1.Retailer_code = gds2.Retailer_code
                                       """
            cursor.execute(query, (n1.Product_number, n2.Product_number, anno))

            for row in cursor:
                result.append(row['peso'])

            cursor.close()
            cnx.close()

        return result[0]

