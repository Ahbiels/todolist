from conn import cursor, conn, Error

class TodoList:
    task = ''
    id_task = None
    user_id = None
    
    @classmethod
    def set_task(cls, user_id, task):
        cls.task = task
        cls.user_id = user_id
        
        if task and user_id:
            try:
                query = "INSERT INTO todolist (user_id, task) VALUES (%s,%s);"
                values = (cls.user_id, cls.task)
                cursor.execute(query, values)
                conn.commit()
            except Error as err:
                print(err)
                # criar uma página de error depois
    
    @classmethod
    def all_task_by_user(cls,user_id):
        cls.user_id = user_id
        if user_id:
            try:
                query = "SELECT id, task FROM todolist WHERE user_id = (%s)"
                cursor.execute(query, (cls.user_id,))
                results = cursor.fetchall()
                tasks = [
                    {"id": result[0], "task":result[1]}
                    for result in results
                ]
                return tasks
            except Error as err:
                print(err)
                # criar uma página de error depois
    
    @classmethod
    def delete_task(cls, id):
        cls.id_task = id
        try:
            query = "DELETE FROM todolist WHERE id = (%s)"
            cursor.execute(query, (cls.id_task,))
            conn.commit()
        except Error as err:
            print(err)
            # criar uma página de error depois
        
        