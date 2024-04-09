import datetime
import sqlite3


       
class Medicament ():
        
        def __init__(self,  name, quantity, use ) :
               
                self.name = name

                self.quantity = quantity

                self.use = use 
                     
        def func(self):
                
                global deadline, enventorydate

                enventorydate = datetime.datetime.now().strftime('%d %b %y')

                days = self.quantity / self.use

                deadline = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime('%d %b %y')

                return self.name,enventorydate, self.quantity, self.use,  deadline
        
class DataBase(Medicament)  :    
        def __init__(self, db_name,  *arg ):
            super().__init__(*arg)
          
            
            self.conn = sqlite3.connect(db_name)

            self.cur = self.conn.cursor()

            self.conn.commit()

        def Insert(self):
                
               
                self.cur.execute(f""" Insert into scheduling  (Name, inventoryDate, Quantity, usage,
                                Deadline) values (?, ?, ?, ?, ?) """,
                                    ( self.name, enventorydate, self.quantity, self.use,  deadline ))
                
                self.conn.commit()

        @classmethod

        def Select(self, db_name  ):
                
                self.conn = sqlite3.connect(db_name)

                self.cur = self.conn.cursor()
               
                self.cur.execute("""select * from scheduling """)

                self.conn.commit()

                return  self.cur.fetchall()

        def Update(self, updateFromname ):
            
                self.cur.execute(f"""  update  scheduling set Name = ? , inventoryDate = ?, 
                                Quantity =   ?, 
                                usage = ?,
                                Deadline = ? where Name = ? """, (self.name, enventorydate, self.quantity, self.use, deadline, updateFromname))
                

                self.conn.commit()

if __name__ == '__main__':

    while True:

        print('======Medicament deadline=========')
        print("     Choissez option :")
        print("     Ajouter remède, Tapez 1")
        print("     info Détails, Tapez 2")
        print("     Actualiser info, Tapez 3")
        answer = input('    >')

        if answer == "1" :

            name = input('   Le nom de medicament : ')

            try: 
                q = int(input('   Quantité: '))

                u = int(input('   Utilisation: '))

                med = Medicament(name, q, u)

                array  = med.func()
                
                print(array)

                try:
                    db = DataBase('medicament.db',name, q, u)
                
                    db.Insert()
                except:
                    print('La base de donnée est inconnue')
                
            except:
                print('    Quatanté et utilisation sont des numeros')

        elif answer == "2":
            
                db = DataBase.Select('medicament.db')
                
                
                print('Med', 'DE', 'Quantité', 'Usage', 'à', "Actuel Stock")
                for item in db:
                    date = datetime.datetime.strptime(item[1],'%d %b %y')
                    current_quantity = item[2] - (datetime.datetime.now() - date).days
                    print(item[0],'|', item[1],'|', item[2] ,'|', item[3] ,'|', item[4],'|', current_quantity)
                    print('------------------------------------------')

        elif answer == "3":
            # try:
                
                updated = input('    le nom de medicament à acuatliser: ')

                name = input('   Le nom de medicament : ')

                q = int(input('   Quantité: '))

                u = int(input('   Utilisation: '))

                med = Medicament( name, q, u)

                array  = med.func()

                db = DataBase('medicament.db', name, q, u)

                db.Update(updated)
            # except:
            #       print('    Le medicament n\'est pas éxisté')
        else:
            False

        

