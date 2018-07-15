from suds.client import Client
from lxml import etree
import os

class pyOBIEE:
    __wsdlURL = None
    __username = None
    __password = None
    __client = None
    __sessionID = None
    __rowDelimiter = "\n"
    __fieldDelimiter = ";"
    __XMLQueryExecutionOptions = None
    __XMLQueryOutputFormat = None

    def __init__(self, wsdlURL, username, password):
        self.__wsdlURL = wsdlURL
        self.__username = username
        self.__password = password
        self.__client = Client(self.__wsdlURL)

    def Login(self):
        try:
            self.__sessionID = self.__client.service["SAWSessionService"].logon(self.__username, self.__password)
            self.SetQueryOptions()
            return True
        except:
            return False
    
    def LoggedIn(self):
        if self.__sessionID == None:
            return False
        else:
            return True

    def SetDelimiters(self, fieldDelimiter=None, rowDelimiter=None):
        if fieldDelimiter != None:
            self.__fieldDelimiter = fieldDelimiter
        if rowDelimiter != None:
            self.__rowDelimiter = rowDelimiter

    def SetQueryOptions(self, maxRowsPerPage=1000):
        if self.__XMLQueryExecutionOptions == None:
            self.__XMLQueryExecutionOptions = self.__client.factory.create("XMLQueryExecutionOptions")
            self.__XMLQueryOutputFormat = self.__client.factory.create("XMLQueryOutputFormat")

        self.__XMLQueryExecutionOptions.async = True
        self.__XMLQueryExecutionOptions.maxRowsPerPage = maxRowsPerPage
        self.__XMLQueryExecutionOptions.refresh = False
        self.__XMLQueryExecutionOptions.presentationInfo = False

    def Logout(self):
        return True
    
    def Get(self, sqlFile, fileName=None):
        if not self.LoggedIn:
            return False
        sql = self.__readFile(sqlFile)
        xmlData = self.__GetData(sql)

        if fileName == None:
            fileName = os.path.basename(sqlFile)[:-4] + '.csv'
        if xmlData == False:
            return False

        try:
            fileHandler = open(fileName, "w")

            rowsetNS = "{urn:schemas-microsoft-com:xml-analysis:rowset}"
            tree = etree.fromstring(xmlData)

            colNames = tree.xpath("//xsd:element/@*[name()='saw-sql:displayFormula']",
                                namespaces={"xsd":
                                            "http://www.w3.org/2001/XMLSchema"})

            columnIDs = tree.xpath("//xsd:element/@name",
                                    namespaces={"xsd":
                                                "http://www.w3.org/2001/XMLSchema"})


            fileHandler.write(self.__fieldDelimiter.join(colNames) + self.__rowDelimiter)
            
            for rowset in tree.findall("*"):
                for row in rowset.findall("*"):
                    if row.tag == rowsetNS + "Row":
                        # walk through all schema fields
                        # check if there is data available for current schema field, if not add blank entry & increase offset
                        cols = row.findall("*")
                        offset = 0
                        rowFields = list()
                        for columnId in range(len(columnIDs)):
                            if (columnId - offset) >= len(cols) or cols[columnId-offset].tag != rowsetNS+columnIDs[columnId]:
                                rowFields.append("")
                                offset = offset+1
                            else:
                                if cols[columnId-offset].text != None:
                                    rowFields.append(cols[columnId-offset].text)
                                else:
                                    rowFields.append("")

                        # do not add rowRecord to output if it's just a blank line
                        rowRecord = self.__fieldDelimiter.join(rowFields) + self.__rowDelimiter
                        if rowRecord != self.__rowDelimiter:
                            fileHandler.write(rowRecord)

            fileHandler.close()
            return True
        except Exception as e:
            print(e)
            return False

    def __GetData(self, sql):
        try:
            buff = ""
            response = self.__client.service["XmlViewService"].executeSQLQuery(sql, self.__XMLQueryOutputFormat.SAWRowsetSchemaAndData,
                                                                self.__XMLQueryExecutionOptions, self.__sessionID)
            
            if response.rowset != None:
                buff += response.rowset

            while response.finished == False:
                response = self.__client.service["XmlViewService"].fetchNext(response.queryID, self.__sessionID)
                if response.rowset != None:
                    buff += response.rowset

            buff = "<xml>" + buff + "</xml>"
            return buff
        except:
            return False

    def __readFile(self, fileName):
        try:
            f = open(fileName, "r")
            output = f.read()
            f.close()
            return output
        except:
            return False

    def __writeFile(self, fileName, str):
        try:
            f = open(fileName, "w")
            f.write(txt)
            f.close()
            return True
        except:
            return False