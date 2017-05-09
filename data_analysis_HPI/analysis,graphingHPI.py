import quandl
import pandas as pd
import pickle  # pickle saves any python object eg variable,lists etc
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

api_key = 'vhkrsKz3TmUN6Qa4QjZK'


# df=quandl.get('FMAC/HPI_AK',authtoken=api_key) #get the dataframe for python by clicking the python button in quandl
# to get all the states from the link https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States

def state_list():
    list_states = pd.read_html('https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States')

    # print(list_states)

    # print(list_states[0][1]) # we need the col 1 of first dataframe
    return list_states[0][1][2:]  # returns a list and  puts list of dataframes


def grab_initial_state_data():
    states = state_list()
    main_df = pd.DataFrame()

    for abbv in states:
        query = "FMAC/HPI_" + str(abbv)  # getting the string for the data frame
        print(query)
        df = quandl.get(query, authtoken=api_key)  # we will be using join as the data frames already have an index
        df.rename(columns={'Value': str(abbv)}, inplace=True)
        df[abbv] = (df[abbv] - df[abbv][0]) / df[abbv][
            0] * 100.00  # percent change of a state wrt to initial value of the state
        if main_df.empty:  # we now need to append all the dataframes together
            main_df = df
        else:
            main_df = main_df.join(df)

    print(main_df.head())
    pickle_out = open('states_percent_change.pickle', 'wb')  # saving the data in a pickle...wb to write as binary
    pickle.dump(main_df, pickle_out)  # copying the data in a new file
    pickle_out.close()


def HPI_US():  # gets the HPI of US as a whole
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df.rename(columns={'Value': "United States"}, inplace=True)
    df['United States'] = (df['United States'] - df['United States'][0]) / df['United States'][0] * 100.00
    print(df.head())
    return df


# grab_initial_state_data()
# once our data has been pickled we don't need to get the data again. So the function is commented
pickle_in = open('states_percent_change.pickle', 'rb')
HPI_data = pickle.load(pickle_in)
# benchmark = HPI_US()

# print(HPI_data.head())
# we can also use pandas own pickle method
# HPI_data.to_pickle('a.pickle')
# HPI_2=pd.read_pickle('a.pickle')

HPI_data_correlation = HPI_data.corr()  # generates a corelation table for all the columns. Very nice function
print(HPI_data_correlation)
print(HPI_data_correlation.describe())  # gives other usefull information

fig = plt.figure()
ax1 = plt.subplot2grid((1, 1), (0, 0))  # creates a 1 by 1 grid starting at (0,0)
# HPI_data.plot(ax=ax1)  # can plot an entire data like this dataframe.plot()
# benchmark.plot(ax=ax1, color='black', linewidth=10)
# all the data starts from one point in the graph meaning all the calculations were done starting from here
# however this is not good. We can use percent change
plt.legend().remove()
plt.show()
