from __init__ import CURSOR, CONN

class Department:
    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS departments"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, location):
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        if self.id in type(self).all:
            del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        department = cls.all.get(row[0])
        if department:
            department.name = row[1]
            department.location = row[2]
        else:
            department = cls(row[1], row[2], id=row[0])
            cls.all[row[0]] = department
        return department

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM departments"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM departments WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM departments WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
