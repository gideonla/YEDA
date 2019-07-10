from emailverifier import Client
from emailverifier import exceptions
import sys

email_input=sys.argv[1]

client = Client('at_R7WZRaWHuRFs2NKrai4VhZ8Fzv2wi')

try:
    data = client.get(email_input)
except exceptions.HttpException:
# If you get here, it means service returned HTTP error code
    pass
except exceptions.GeneralException:
# If you get here, it means you cannot connect to the service
    pass
except exceptions.UndefinedVariableException:
# If you get here, it means you forgot to specify the API key
    pass
except exceptions.InvalidArgumentException:
# If you get here, it means you specified invalid argument
# (options should be a dictionary)
    pass
except:
    pass
# Something else happened related. Maybe you hit CTRL-C
# while the program was running, the kernel is killing your process, or
# something else all together.

print(data)
