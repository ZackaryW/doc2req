
def preprocess_dict(data :dict): # type: ignore
    """
    ! this is not a generic function, i observed that the data presented in my testcase is a dict of dict of list
    """

    if data is None:
        return []
    
    if len(data) == 0:
        return []
    
    if "fields" not in data:
        return []

    data :dict = data.pop("fields" )
    new_list : list = []

    for k, v in data.items():
        new_list :list = new_list + v
    
    return new_list
    