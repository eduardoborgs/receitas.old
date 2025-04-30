File "/mount/src/receitas/app.py", line 89, in <module>
    st.download_button(
File "/home/adminuser/venv/lib/python3.12/site-packages/streamlit/runtime/metrics_util.py", line 444, in wrapped_func
    result = non_optional_func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/streamlit/elements/widgets/button.py", line 528, in download_button
    return self._download_button(
           ^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/streamlit/elements/widgets/button.py", line 815, in _download_button
    element_id = compute_and_register_element_id(
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/streamlit/elements/lib/utils.py", line 239, in compute_and_register_element_id
    _register_element_id(ctx, element_type, element_id)
File "/home/adminuser/venv/lib/python3.12/site-packages/streamlit/elements/lib/utils.py", line 145, in _register_element_id
    raise StreamlitDuplicateElementId(element_type)
