import pandas as pd
import scipy.stats
import streamlit as st
import time

# These variables are preserved between app reruns
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

st.header('Tossing a Coin')

# Chart to display the running mean
chart = st.line_chart([0.5])

# Simulate the coin toss
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

# User controls
number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

# When user clicks "Run"
if start_button:
    st.write(f'Running the experiment of {number_of_trials} trials.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)

    # Store results in DataFrame
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'], number_of_trials, mean]],
                     columns=['no', 'iterations', 'mean'])
    ], axis=0)

    # Reset index
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

    # Display the table
    st.write(st.session_state['df_experiment_results'])