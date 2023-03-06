global disabled  # boolean for disable card or not
global owed  # return value of total owed amount
global owed_interest  # value of total interest amount
global owed_current  # value of total current amount
global countries  # array to save countries purchased from
global data  # array to save amounts owed
global data_i  # array to save interest compounding values
global calculated_already  # array to keep track of only 1 interest calculation per month
# vars for operation same day or later:
global latest_day  # saves most recent date a function was called
global latest_month  # saves most recent month a function was called


def initialize():
    # set up global vars
    global owed
    global owed_interest
    global owed_current
    global countries
    global disabled
    global data
    global latest_day
    global latest_month
    global data_i
    global calculated_already
    # assume the earliest date possible before starting program is Jan 1.
    latest_day = 1
    latest_month = 1
    # set up other initial conditions
    disabled = False
    owed_interest = 0
    owed_current = 0
    owed = owed_interest + owed_current
    countries = []  # empty for now, will be filled with string elements
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # values stored for each month.
    # making it 13 indexes so that indexing can start at 1 to match month (data[0] wont be used)
    data_i = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    calculated_already = [None, False, False, False, False, False, False, False, False, False, False, False, False]


def date_same_or_later(day1, month1, day2, month2):
    # return boolean for if date is later than saved date, given two dates and months
    if month1 > month2:
        return True
    elif month1 == month2:
        if day1 > day2:
            return True
        elif day1 == day2:
            return "Same"  # Guide says to make this also return True, but since I will be using this function
            # I need it to only return True if its later (for operation on later date)
    return False


def all_three_different(c1, c2, c3):
    # return boolean depending on if three parameters c1, c2, c3 are all different
    # this is used for the 3 countries disable mechanism
    if c1 == c2 or c2 == c3 or c1 == c3:
        return False
    return True


def purchase(amount, day, month, country):
    # make a purchase of amount on day, month, in country
    # day and month must be real on the calendar (ints, day <= 31, month <=12), amount must be an int
    # country must be a String
    global latest_day
    global latest_month
    global disabled
    global owed
    global owed_interest
    global owed_current

    operation_later = date_same_or_later(latest_day, latest_month, day, month)
    if operation_later == True:
        return "error"

    # deactivate check:
    if deactivate_check(country) == True or disabled == True:
        # checks if card is disabled or should be disabled
        disabled = True
        return "error"
        # will disable card and won't proceed with purchase
    else:
        countries.append(country)
        # data matrix:
        # ex: [0, 80, 50, 40, 0, 0, 10, 100, 30]
        # index n = amount bought in month n
        # ex: index 1 = $80 in jan, index 2 = $50 in feb.
        # since month is an int value, we can operate on it easily:
        data[month] += amount
        # update latest day, month
        latest_day = day
        latest_month = month


def amount_owed(day, month): # return the amount owed in total at date of day, month
    # day and month must be real on the calendar (ints, day <= 31, month <=12), amount must be an int
    global latest_day
    global latest_month
    global owed
    global owed_interest
    global owed_current
    global data
    global data_i
    global calculated_already

    operation_later = date_same_or_later(latest_day, latest_month, day, month)
    if operation_later == True:
        return "error"
    else:
        # calculate amount owed
        for i in range(len(data)):
            if month >= i + 2 and calculated_already[month] != True: # prevents calculating interest more than once/month
                # month i+2 is the first month where money from month i starts getting interest

                # compound interest formula: A = P(1.05)^n-1, where n is months after month after payment eg: Bought
                # $100 in Jan, Bill in Jan = $100 (credit), Bill in Feb = $100, Bill in march for jan purchases =$105
                data_i[i] = data[i] * (1.05 ** (month - (i + 1)))
            elif month == i + 1:  # month i+1 is when bill comes back for month i, owed = same amount as purchase
                owed_current = data[i]  # adds it to current owed bill
            elif month == i:
                owed_current += data[i]  # bill for month i techniclaly is 0, but purchase amount is still on credit
                # the split elif statement and += makes sure there's no duplication since month==i+1 goes first,
                # so this will be added to the total
        owed_interest = sum(data_i)
        owed = owed_current + owed_interest
        # update latest day, month
        latest_day = day
        latest_month = month
        return owed
        # pay_bill(0, day, month)
        # print(owed_interest)
        # print(owed_current)
        # print(owed)
        # return owed


def pay_bill(amount, day, month): # allow the user to pay amount and deduct their owed by amount on day, month
    # day and month must be real on the calendar (ints, day <= 31, month <=12), amount must be an int
    global latest_day
    global latest_month
    global owed
    global owed_interest
    global owed_current
    global calculated_already

    operation_later = date_same_or_later(latest_day, latest_month, day, month)
    if operation_later == True:
        return "error"
    else:
        # case 1: amount <= owed interest
        # case 2: amount > owed interest but < owed total
        # case 3: amount >= owed total (owed interest + owed current), not tested

        # IMPORTANT: First need to calculate interests based on date of bill payment (similar to amount owed function)
        # calculate amount (same code as in amount_owed, this is used to tally up current and interest by payment day)
        amount_owed(day, month)

        if sum(data_i) != 0:  # if there is INTEREST
            # objective: subtract interest from total and prioritize which interest to
            # subtract from: the one with the most accruing interest will be prioritized (highest value in data_i
            # calculated from amount_owed function)
            while amount > 0:  # run until all amount deducted
                if amount < max(data_i):
                    temp_index = data_i.index(max(data_i))
                    data_i[data_i.index(max(data_i))] -= amount  # max element of data_i subtract amount
                    amount = 0  # get rid of all amount

                    # update value in data[] list
                    # eg: $100 in data accrued to $105 in data_i, payment of $100 -> data_i = $5, update data = $5
                    # this helps with recalculating in next function called
                    data[month - 1] += data_i[temp_index]
                    data[temp_index] = 0
                    data_i[temp_index] = 0
                    # issue appears: IF in the scenario where user pays bill on interest, interest is now updated
                    # when calculating amount owed for the same month, interest calculation will take newly updated
                    # data[temp_index] and calculate interest again (need to limit only 1 interest calculation/month)
                    calculated_already[month] = True

                else:  # if amount is greater than the most interest accruing element
                    amount -= max(data_i)  # recalculates amount remaining
                    temp_index = data_i.index(max(data_i))
                    data_i[data_i.index(max(data_i))] = 0  # deducts all interest, recalculates for max in next iter.

                    # issue is also here
                    data[month - 1] += data_i[temp_index]
                    data[temp_index] = 0
                    data_i[temp_index] = 0
                    calculated_already[month] = True

                    if sum(data_i) == 0:
                        break  # breaks loop if all interest paid off as well

            # check which condition caused while loop to exit, i.e: if all interest paid off:
            if sum(data_i) == 0:
                # remove remaining money from currently owed
                # update values in array
                while amount > 0:
                    if amount < max(data[month],
                                    data[month - 1]):  # subtract max of this or last month's (non interest)
                        data[data.index(max(data[month], data[month - 1]))] -= amount
                        amount = 0
                    else:  # amount is greater than one max
                        amount -= max(data[month], data[month - 1])
                        data[data.index(max(data[month], data[month - 1]))] = 0
                        if data[month] + data[month - 1] == 0:
                            break  # break if all paid off

                if data[month] + data[month - 1] == 0:  # amount is more than all owed debt
                    owed_current = 0
                    data[month] = 0  # pays off all credit this month and prev month
                    data[month - 1] = 0
                    print("All debt paid, amount remaining is " + str(amount))

        else:  # if only owed current present
            # update values in array
            while amount > 0:
                if amount < max(data[month], data[month - 1]):  # subtract max of this or last month (both non interest)
                    data[data.index(max(data[month], data[month - 1]))] -= amount
                    amount = 0
                else:  # amount is greater than one max
                    amount -= max(data[month], data[month - 1])
                    data[data.index(max(data[month], data[month - 1]))] = 0
                    if data[month] + data[month - 1] == 0:
                        break  # break if all paid off

            if data[month] + data[month - 1] == 0:  # amount is more than all owed debt
                owed_current = 0
                data[month] = 0  # pays off all credit this month and prev month
                data[month - 1] = 0
                print("All debt paid, amount remaining is " + str(amount))

        # update variables
        owed_interest = sum(data_i)
        owed = owed_interest + owed_current
        # update latest day, month
        latest_day = day
        latest_month = month


def deactivate_check(new):
    # check if the card is deactivated (return a boolean)
    # new is the most recent country string passed thru purchase() function
    global countries
    global disabled
    # objective : find three different countries in a row
    # first off, if less than 2 countries are in list, then no disable
    # this avoids out of bounds error in else block
    if len(countries) < 2:
        return False
    else:
        if all_three_different(new, countries[-1], countries[-2]):
            # if the recent 2 consecutive countries in the list are different
            # from each other and from the third newly inputted country
            return True
        return False


# testing
if __name__ == "__main__":
    initialize()

    # self testing:
    # purchase(80, 8, 1, "Canada")
    # purchase(80, 8, 2, "Canada")
    # purchase(80, 8, 3, "Canada")
    # print(data)
    # print("Now owing:", amount_owed(8, 4))
    # print(data_i)
    # print(pay_bill(350, 8, 9))
    # pay_bill(50, 2, 2)
    # print("Now owing:", amount_owed(2, 2))

    # recommended testing:
