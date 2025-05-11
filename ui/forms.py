def render_strategy_params(params_def):
    import streamlit as st
    result = {}
    for name, info in params_def.items():
        ptype = info['type']
        default = info['default']
        if ptype == int:
            result[name] = st.number_input(f"{name}", value=default, step=1)
        elif ptype == float:
            result[name] = st.number_input(f"{name}", value=default, step=0.1)
        elif ptype == bool:
            result[name] = st.checkbox(f"{name}", value=default)
        elif ptype == str:
            result[name] = st.text_input(f"{name}", value=default)
    return result