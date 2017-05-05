import quandl
import pandas as pd
import pickle

# pickle saves any python object eg variable,lists etc

api_key = 'vhkrsKz3TmUN6Qa4QjZK'


# df=quandl.get('FMAC/HPI_AK',authtoken=api_key) #get the dataframe for python by clicking the python button in quandl
# print(df.head())

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
        df = quandl.get(query, authtoken=api_key)  # we will be using join as the data frames already have an index
        df.rename(columns={'Value': str(abbv)}, inplace=True)
        if main_df.empty:  # we now need to append all the dataframes together
            main_df = df
        else:
            main_df = main_df.join(df)

    print(main_df.head())
    pickle_out = open('states.pickle', 'wb')  # saving the data in a pickle...wb to write as binary
    pickle.dump(main_df, pickle_out)  # copying the data in a new file
    pickle_out.close()

# grab_initial_state_data()
# once our data has been pickled we don't need to get the data again. So the function is commented
pickle_in=open('states.pickle','rb')
HPI_data=pickle.load(pickle_in)
print(HPI_data)
# we can also use pandas own pickle method
# HPI_data.to_pickle('a.pickle')
# HPI_2=pd.read_pickle('a.pickle')
