def check_args(args: str) -> str:
    """get the filename from the command line arguments

    Args:
        args (str): command line arguments

    Returns:
        str: filename
    """
    resolution = -1
    filename = ""
    execute = False
    
    # python .\src\main.py -r 1200 -f .\games\board_template.txt (the order of the arguments does not matter)
    
    if "-r" in args:
        try:
            resolution = int(args[args.index("-r") + 1])
        except:
            print("Invalid resolution")
            resolution = -1
    
    if "-f" in args:
        filename = args[args.index("-f") + 1]
        
    if "-e" in args:
        execute = True
        
    return filename, resolution, execute