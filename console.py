#!/usr/bin/python3
"""
command line interpreter for AirBnB
"""

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
        HBNBC - a console class for the the airbnb clone
        program
    """

    prompt = '(hbnb) '
    __class_lst = {
        BaseModel.__name__: BaseModel,
        User.__name__: User,
        State.__name__: State,
        City.__name__: City,
        Place.__name__: Place,
        Amenity.__name__: Amenity,
        Review.__name__: Review
    }
    __class_funcs = ["all", "count", "show", "destroy", "update"]

    @staticmethod
    def parse(arg, id=" "):
        """
        Returns a list conatning the parsed arguments from the string
        """

        arg_ls = arg.split(id)
        new_arg_ls = []

        for x in arg_ls:
            if x != '':
                new_arg_ls.append(x)
        return new_arg_ls

    def do_quit(self, arg):
        """Exits the program"""

        return True

    def do_EOF(self, arg):
        """Exits the program"""

        print("")
        return True

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
        """
        try:
            class_name = arg.split(" ")[0]
            if len(class_name) == 0:
                print("** class name missing **")
                return
            if class_name and class_name not in self.valid_classes:
                print("** class doesn't exist **")
                return

            kwargs = {}
            commands = arg.split(" ")
            for i in range(1, len(commands)):
                
                key = commands[i].split("=")[0]
                value = commands[i].split("=")[1]
                #key, value = tuple(commands[i].split("="))
                if value.startswith('"'):
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                new_instance = eval(class_name)()
            else:
                new_instance = eval(class_name)(**kwargs)
            storage.new(new_instance)
            print(new_instance.id)
            storage.save()
        except ValueError:
            print(ValueError)
            return
        
    def do_show(self, arg):
        """
            Prints the string representation of an instance based
            on the class name and id.
        """
        arg_lst = HBNBCommand.parse(arg)
        db = storage.all()
        if not len(arg_lst):
            print("** class name missing **")
        elif (arg_lst[0] not in HBNBCommand.__class_lst.keys()):
            print("** class doesn't exist **")
        elif len(arg_lst) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_lst[0], arg_lst[1]) not in db:
            print("** no instance found **")
        else:
            print(db["{}.{}".format(arg_lst[0], arg_lst[1])])

    def do_destroy(self, arg):
        """
            Deletes an instance based on the class name and id
            (save the change into the JSON file).
        """
        arg_lst = HBNBCommand.parse(arg)
        storage.reload()
        db = storage.all()
        if not len(arg_lst):
            print("** class name missing **")
        elif (arg_lst[0] not in HBNBCommand.__class_lst.keys()):
            print("** class doesn't exist **")
        elif len(arg_lst) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_lst[0], arg_lst[1]) not in db:
            print("** no instance found **")
        else:
            # print(storage.__class__.__name__.__objects)
            del db["{}.{}".format(arg_lst[0], arg_lst[1])]
            storage.save()

    def do_all(self, arg):
        """
            Prints all string representation of all instances based or
            not on the class name.
        """
        arg_ls = HBNBCommand.parse(arg)
        if len(arg_ls) > 0 and arg_ls[0] not in HBNBCommand.__class_lst:
            print("** class doesn't exist **")
        else:
            obj1 = []
            for obj in storage.all().values():
                if len(arg_ls) > 0 and arg_ls[0] == obj.__class__.__name__:
                    obj1.append(obj.__str__())
                elif len(arg_ls) == 0:
                    obj1.append(obj.__str__())
            print(obj1)

    def do_update(self, arg):
        """
            Updates an instance based on the class name and id by adding or
            updating attribute (save the change into the JSON file).
        """
        arg_ls = HBNBCommand.parse(arg)
        obj_dict = storage.all()

        if len(arg_ls) == 0:
            print("** class name missing **")
            return False
        if arg_ls[0] not in HBNBCommand.__class_lst:
            print("** class doesn't exist **")
            return False
        if len(arg_ls) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_ls[0], arg_ls[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_ls) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_ls) == 3:
            try:
                type(eval(arg_ls[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(arg_ls) == 4:
            obj = obj_dict["{}.{}".format(arg_ls[0], arg_ls[1])]
            if arg_ls[2] in obj.__class__.__dict__.keys():
                value_type = type(obj.__class__.__dict__[arg_ls[2]])
                obj.__dict__[arg_ls[2]] = value_type(arg_ls[3])
            else:
                obj.__dict__[arg_ls[2]] = arg_ls[3]
        elif type(eval(arg_ls[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_ls[0], arg_ls[1])]
            for k, v in eval(arg_ls[2]).items():
                if (k in obj.__class__.__dict__.keys() and type(
                        obj.__class__.__dict__[k]) in {str, int, float}):
                    value_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = value_type(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def emptyline(self):
        """
            Does nothing if Empty line + enter is inserted.
        """
        pass

    def do_count(self, arg):
        """
            prints the number of elements inside the FileStorage
        """
        arg_ls = HBNBCommand.parse(arg)
        if len(arg_ls) > 0 and arg_ls[0] not in HBNBCommand.__class_lst:
            print("** class doesn't exist **")
        else:
            obj1 = []
            for obj in storage.all().values():
                if len(arg_ls) > 0 and arg_ls[0] == obj.__class__.__name__:
                    obj1.append(obj.__str__())
                elif len(arg_ls) == 0:
                    obj1.append(obj.__str__())
            print(len(obj1))

    def show(self, cls):
        """
            Gives all the elements inside the FileStorage that
            are of instances of cls
        """
        pass

    def destroy(self, cls):
        """
            Gives all the elements inside the FileStorage that
            are of instances of cls
        """
        pass

    def update(self, cls):
        """
            Gives all the elements inside the FileStorage that
            are of instances of cls
        """
        pass

    def default(self, line):
        """
            Handles the case where the the command has no equivilant
            do_ method
        """

        line = HBNBCommand.parse(line, '.')
        if line[0] in HBNBCommand.__class_lst.keys() and len(line) > 1:
            if line[1][:-2] in HBNBCommand.__class_funcs:
                func = line[1][:-2]
                cls = HBNBCommand.__class_lst[line[0]]
                eval("self.do_" + func)(cls.__name__)
            else:
                print("** class doesn't exist **")
        else:
            super().default(line)
        return False


if __name__ == "__main__":
    console = HBNBCommand()
    console.cmdloop()
