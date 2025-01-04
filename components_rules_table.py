import streamlit as st
import pandas as pd
from utils import *

def render_rules_table():
    # Pull from rules_dict instead of "rules"
    rules_dict = st.session_state.get("rules_dict", {})

    if rules_dict:
        num_rules = len(rules_dict)
        st.success(f"Generated {num_rules} Association Rules")

        # Convert dict to a list for display
        rules_list = []
        for rule_index, rule_data in rules_dict.items():
            rules_list.append((
                rule_data["antecedent"],
                rule_data["consequent"],
                rule_data["confidence"],
                rule_data["lift"],
                rule_data["conviction"]
            ))

        options = generate_pagination_options(num_rules)
        num_to_show = st.selectbox("Select number of rules to show per page", options, key="num_to_show")
        
        if num_to_show:
            # Create a DataFrame from rules_list
            rules_df = pd.DataFrame([
                {
                    'Antecedent': ', '.join(sorted(list(r[0]))),
                    'Consequent': ', '.join(sorted(list(r[1]))),
                    'Confidence': round(r[2], 2),
                    'Lift': round(r[3], 2),
                    'Conviction': round(r[4], 2) if r[4] is not None else 'Infinity'
                }
                for r in rules_list
            ])
            rules_df.sort_values(by='Confidence', ascending=False, inplace=True)            
            data_to_show = rules_df if num_to_show == "All" else rules_df.head(num_to_show)
            data_to_show.reset_index(drop=True, inplace=True)
            data_to_show.index += 1
            st.write(f"### Top {num_to_show} Rules sorted by confidence:")
            st.table(data_to_show)
        else:
            st.warning("No rules to show.")
    else:
        st.warning("No rules generated with the given minimum confidence.")