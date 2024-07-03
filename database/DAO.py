from database.DB_connect import DBConnect
from model.country import Country
from model.contiguity import Contiguity


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from country"
        cursor.execute(query)

        for row in cursor:
            result.append(Country(row["StateAbb"], row["CCode"], row["StateNme"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(year, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select state1no, state2no
        from contiguity
        where year <= %s and conttype = 1
        group by dyad
        """
        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Contiguity(idMap[row["state1no"]],
                                     idMap[row["state2no"]]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(year, idMap): # prende tutti gli edges senza filtrare conttype
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            select state1no, state2no
            from contiguity
            where year <= %s
            group by dyad
            """
        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Contiguity(idMap[row["state1no"]],
                                     idMap[row["state2no"]]))
        cursor.close()
        conn.close()
        return result
