#!/usr/bin/python3
"""AirBnB Console"""

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = ['BaseModel', 'User', 'Place', 'State', 'City', 'Amenity', 'Review']


class HBNBCommand(cmd.Cmd):
    """The command interpreter of AirBnB project"""
    prompt = '(hbnb) '

    def do_create(self, args):
        """Create a new instance of a class and prints the id"""
        try:
            class_name = args.split(" ")[0]
        except:
            indexError
            pass
        if len(class_name) == 0:
            print("** class name missing **")
        elif class_name not in classes:
            print("** class doesn't exist **")
        else:
            all_list = args.split(" ")
            new_instance = eval(class_name)()
            for i in range(1, len(all_list)):
                key, value = tuple(all_list[i].split("="))
                if value.startswith('"'):
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except:
                        exception
                        print(f"{value} couldnot evaluate")
                        pass
                if hasattr(new_instance, key):
                    setattr(new_instance ,key, value)
        storage.new(new_instance)
        print(new_instance.id)
        new_instance.save()



    def do_show(self, args):
        """Prints the json file of an instance of a class name and id"""
        words = args.split(' ')
        if len(args) == 0:
            print("** class name missing **")
            return
        elif words[0] not in classes:
            print("** class doesn't exist **")
            return
        elif len(words) == 1:
            print("** instance id missing **")
            return
        all_objs = storage.all()
        s = words[0] + '.' + words[1]
        for obj_id in all_objs.keys():
            if s == obj_id:
                obj = all_objs[obj_id]
                print(obj)
                return
        print("** no instance found **")
        pass

    def do_all(self, args):
        """Prints all string representation of all instances"""
        if len(args) == 0:
            all_objs = storage.all()
            new_list = []
            for obj_id in all_objs.keys():
                obj = all_objs[obj_id]
                new_list.append("{}".format(obj))
            print(new_list)
        elif args not in classes:
            print("** class doesn't exist **")
        elif args in classes:
            all_objs = storage.all()
            for obj_id in all_objs.keys():
                key1 = obj_id.split('.')
                if key1[0] == args:
                    obj = all_objs[obj_id]
                    print("{}".format(obj))

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""
        words = args.split(' ')
        if len(args) == 0:
            print("** class name missing **")
            return
        elif words[0] not in classes:
            print("** class doesn't exist **")
            return
        elif len(words) == 1:
            print("** instance id missing **")
            return
        all_objs = storage.all()
        s = words[0] + '.' + words[1]
        for key, value in all_objs.items():
            if s in key:
                del all_objs[str(s)]
                storage.save()
                return
        print("** no instance found **")

    def do_update(self, args):
        """Updates an instance based on the class name and id
        by adding or updating attribute"""
        words = args.split(' ')
        if len(args) == 0:
            print("** class name missing **")
            return
        elif words[0] not in classes:
            print("** class doesn't exist **")
            return
        elif len(words) == 1:
            print("** instance id missing **")
            return
        if len(words) == 3:
            print("** value missing **")
            return
        s1 = words[0] + '.' + words[1]
        all_objs = storage.all()
        for key, value in all_objs.items():
            if s1 in key:
                if len(words) == 2:
                    print("** attribute name missing **")
                    return
                if words[3][0] == "\"" and words[3][-1] == "\"":
                    setattr(value, words[2], words[3][1:-1])
                    storage.save()
                    return
                setattr(value, words[2], words[3])
                storage.save()
                return
        print("** no instance found **")

    def precmd(self, line):
        """Reformat command line for advanced command syntax.
        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] is '{' and pline[-1] is '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def do_count(self, line):
        """
        Counts number of instances of a class
        """
        all_objs = storage.all()
        count = 0
        for name in all_objs:
            if name[0:len(line)] == line:
                count += 1
        print(count)

    def emptyline(self):
        """Method called when an empty line is entered in response
        to the prompt"""
        pass

    def do_EOF(self, line):
        """Ctrl D - the program will exit cleanly"""
        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

if __name__ == '__main__':
    HBNBCommand().cmdloop()
