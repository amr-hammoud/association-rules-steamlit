import streamlit as st
import pandas as pd
from utils import *

def render_rules_table():
  rules = st.session_state.get("rules", [])
  if rules:
      num_rules = len(rules)
      st.success(f"Generated {num_rules} Association Rules")
      options = generate_pagination_options(num_rules)
      num_to_show = st.selectbox("Select number of rules to show per page", options, key="num_to_show")
      
      if num_to_show:
          rules_df = pd.DataFrame([
              {
                  'Antecedent': ', '.join(sorted(list(rule[0]))),
                  'Consequent': str(rule[1]),
                  'Confidence': round(rule[2], 2),
                  'Lift': round(rule[3], 2),
                  'Conviction': round(rule[4], 2) if rule[4] is not None else 'Infinity'
              }
              for rule in rules
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