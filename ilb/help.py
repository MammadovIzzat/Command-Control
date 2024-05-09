
def help():
    HELP = """
    COMMANDS    Usage                            DESCRIPTION
    ---------   ------------------------------   -----------
    connect     connect <NickName>               Connect to Spesific Host
                close                            Close Connection
                ftp <-d/-u> <data>               FTP server has two option -d, -u
                    -d                           Download file from client to ./Data/ftp folder
                    -u                           Upload file from ./Data/ftp folder to pwd
    list        list                             Show all Hosts
    nick        nick <HostName> <New NickName>   Assign or Change NickName
    history     history                          Show Command History
                history <HostName>               Show Command History Used in Spesific Host
    start       start <NickName>                 Start Connection
    stop        stop <NickName>                  Stop Connection
    clear       clear                            Clear Terminal
    exit        exit                             Stop Server
    """
    return HELP