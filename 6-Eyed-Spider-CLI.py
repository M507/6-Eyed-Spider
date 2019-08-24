from cmd import Cmd
from Lib.Plugins.ESXI_UI import *


class MyPrompt(Cmd):
    prompt = 'pb> '
    intro = "Welcome! Type ? to list commands"

    def do_exit(self, inp):
        print("Bye")
        #print("adding '{}'".format(inp))
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def do_Add_ESXI_Admin(self, line):
        line = line.split(' ')
        ESXI_IP = line[0]
        USERNAME = line[1]
        STRONG_PASSWORD = line[2]
        Description = line[3]
        print(USERNAME, STRONG_PASSWORD, Description)
        # Check each one of them - REGEX - Then pass them

        # IF good to go:
        # Add_ESXI_Admin 192.168.0.18 BLACK_TEAM Liverpool!1!1! Description1
        Execute_VMware_ESXI(ESXI_IP, 'Add_Admin', USERNAME, STRONG_PASSWORD, Description)

    def help_Add_ESXI_Admin(self):
        print("Add admin user.\n"
              "Usage: Add_ESXI_Admin <ESXI_IP> <USERNAME> <STRONG_PASSWORD> <Description>\n"
              "Add_ESXI_Admin 192.168.1.10 BLACK_TEAM Liverpool!1!1! Description1\n")

    def do_ESXI_Enable_SSH(self, line):
        line = line.split(' ')
        ESXI_IP = line[0]
        # Check - REGEX - Then pass it

        # IF good to go:
        # ESXI_Enable_SSH 192.168.0.18
        Execute_VMware_ESXI(ESXI_IP, 'Enable_SSH')

    def help_ESXI_Enable_SSH(self):
        print("Enable SSH.\n"
              "Usage: ESXI_Enable_SSH <ESXI_IP>\n"
              "ESXI_Enable_SSH 192.168.1.10\n")

    def do_print_creds(self, line):
        line = line.split(' ')
        IP = line[0]

        # Check if ip is real ip - Regex

        # Print it

    def help_print_creds(self):
        print("List all stored credentials.\n"
              "Usage: print_creds <ip>\n"
              "print_creds 192.168.1.10\n"
              "print_creds all")

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        #print("Default: {}".format(inp))
        print("Try again")

    # do_EOF = do_exit
    # help_EOF = help_exit


if __name__ == '__main__':
    MyPrompt().cmdloop()