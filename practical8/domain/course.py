class Course:
    def __init__(self, c_id, name, credits):
        self.__id = c_id
        self.__name = name
        self.__credits = credits

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_credits(self):
        return self.__credits

    def __str__(self):
        return f"ID: {self.__id} | Name: {self.__name} | Credits: {self.__credits}"