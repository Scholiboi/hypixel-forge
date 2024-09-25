from forge import forging, my_resources

def add_resource(name, amount):
    global my_resources, forging
    if name in my_resources:
        my_resources[name] += amount
    else:
        print("That resource doesnt exist.")


def viewItem(name, temp_resources):
    global my_resources, forging
    if name in forging:
        for i in forging[name]:
            if i in temp_resources:
                temp_resources[i] += forging[name][i]
            else:
                temp_resources[i] = forging[name][i]
        return temp_resources
        

def viewBaseItems(name, count=1, iterations=0):
    global my_resources, forging, temp_resources
    if name in forging:
        for i in forging[name]:
            if i in forging:
                viewBaseItems(i, count=count*forging[name][i], iterations=iterations+1)
            else:
                if i in temp_resources:
                    temp_resources[i] += forging[name][i]*count
                else:
                    temp_resources[i] = forging[name][i]*count
    if iterations == 0:
        for i in temp_resources:
            print(f"{i}: {temp_resources[i]}")
        temp_resources = {}
        return None
    else:
        return None


def removeResource(name, amount):
    global my_resources, forging, temp_resources
    if name in forging:
        for i in forging[name]:
            if i in my_resources:
                if my_resources[i] < forging[name][i]*amount:
                    print("You dont have enough resources.")
                    break
                else:
                    my_resources[i] -= forging[name][i]*amount
    else:
        print("That forge item doesnt exist.")


def viewRequirements(name, count=1):
    global my_resources, forging, temp_resources, my_temp_resources
    if name in forging:
        for i in forging[name]:
            if i in forging:
                viewBaseRequirements(i, count = forging[name][i]*count - my_resources[i], iterations=1)
                # base requirements recursion
            else:
                if i in temp_resources:
                    temp_resources[i] += forging[name][i]*count - my_resources[i]
                else:
                    temp_resources[i] = forging[name][i]*count - my_resources[i]
    for i in temp_resources:
        if temp_resources[i] < 0:
            temp_resources[i] = abs(temp_resources[i])
            print(f"{i}: You have {temp_resources[i]} more than you need.")
        elif temp_resources[i] > 0:
            print(f"{i}: You need {temp_resources[i]} more.")
    temp_resources = {}
    return None


def viewBaseRequirements(item, count=1, iterations=0):
    global my_resources, forging, temp_resources
    if item in forging:
        for i in forging[item]:
            if i in forging:
                viewBaseRequirements(i, count = forging[item][i]*count - my_resources[i], iterations=iterations+1)
            else:
                if i in temp_resources:
                    temp_resources[i] += forging[item][i]*count
                else:
                    temp_resources[i] = forging[item][i]*count

