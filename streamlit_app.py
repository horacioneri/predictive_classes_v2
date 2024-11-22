import streamlit as st
import pandas as pd
import numpy as np
from config import page_titles
from sidebar import sidebar_config
from page_body import introduction_text, exploratory_data_analysis, data_preparation, model_training, result_analysis, model_interpretation
import zipfile

# Navigation function with forced rerun
def change_page(delta):
    st.session_state.page = max(0, min(len(page_titles) - 1, st.session_state.page + delta))
    st.session_state.expander_open = False  # Collapse the expander when going to the next page
    st.rerun()  # Force immediate rerun to reflect the updated page state

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = 0

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "treated" not in st.session_state:
    st.session_state.treated = False

if "trained" not in st.session_state:
    st.session_state.trained = False

current_page = st.session_state.page

# Page config
st.set_page_config(page_title='Building a ML model', page_icon='', layout = 'wide')

# Display LTP logo
st.image(image= "images/Asset 6.png", caption = "Powered by", width = 100)

if current_page > 0:
    if st.button("Restart", use_container_width=True, key=f"top_restart_{current_page}"):
        st.session_state.page = 0
        st.session_state.uploaded = False
        st.session_state.df_original = pd.DataFrame()
        st.session_state.df_treated = pd.DataFrame()
        st.rerun()

# Display title of the page
st.title(page_titles[current_page], anchor='title')

# Sidebar for accepting input parameters
sidebar_config(current_page)

if current_page == 0:
    introduction_text()

if current_page == 1:
    if not st.session_state.uploaded:
        st.write('Go back to the previous page and reupload your dataset')
    else:
        exploratory_data_analysis()

if current_page == 2:
    if not st.session_state.uploaded:
        st.write('Go back to the beginning and reupload your dataset')
    else:
        data_preparation()

if current_page == 3:
    if not st.session_state.treated:
        st.write('Go back to the previous page and prepare your dataset')
    else:
        model_training()

if current_page == 4:
    if not st.session_state.trained:
        st.write('Go back to the previous page and train your model')
    else:
        result_analysis()

if current_page == 5:
    if not st.session_state.trained:
        st.write('Go back to the model training page and train your model')
    else:
        model_interpretation()

# Display buttons at the end to navigate between pages
if current_page == 0:
    left, right = st.columns(2)
    if right.button("Next", use_container_width=True, key="next_0"):
        change_page(1)

elif 0 < current_page < len(page_titles)-1:
    left, right = st.columns(2)
    if left.button("Previous", use_container_width=True, key=f"prev_{current_page}"):
        change_page(-1)
    if right.button("Next", use_container_width=True, key=f"next_{current_page}"):
        change_page(1)

elif current_page == len(page_titles)-1:
    left, right = st.columns(2)
    if left.button("Previous", use_container_width=True, key=f"prev_{current_page}"):
        change_page(-1)
# Restart if needed
else:
    st.session_state.page = 0

if current_page > 0:
    if st.button("Restart", use_container_width=True, key=f"bot_restart_{current_page}"):
        st.session_state.page = 0
        st.session_state.uploaded = False
        st.session_state.df_original = pd.DataFrame()
        st.session_state.df_treated = pd.DataFrame()
        st.rerun()
#Please
            
#         st.write("Evaluating performance metrics ...")
#         #time.sleep(sleep_time)
#         if problem_type == 'Regression': 
#             train_mse = mean_squared_error(y_train, y_train_pred)
#         else:
#             train_accuracy = accuracy_score(y_train, y_train_pred)
#             train_conf_matrix = confusion_matrix(y_train, y_train_pred)
#             train_class_report = classification_report(y_train, y_train_pred)

#         if problem_type == 'Regression': 
#             st.write("Train mean squared error:", train_mse)
#         else:
#             st.write("Train model accuracy:", train_accuracy)
#             st.write("Train confusion matrix:", train_conf_matrix)
#             #st.write(train_class_report)
        
#         if problem_type == 'Regression': 
#             test_mse = mean_squared_error(y_test, y_test_pred)
#         else:
#             test_accuracy = accuracy_score(y_test, y_test_pred)
#             test_conf_matrix = confusion_matrix(y_test, y_test_pred)
#             test_class_report = classification_report(y_test, y_test_pred)


#         if problem_type == 'Regression': 
#             st.write("Test mean squared error:", test_mse)
#         else:
#             st.write("Test model accuracy:", test_accuracy)
#             st.write("Test confusion matrix:", test_conf_matrix)
#             #st.write(test_class_report)
        
#         st.write("Displaying performance metrics ...")
#         time.sleep(sleep_time)
#         if problem_type != 'Regression':
#             rf_results = pd.DataFrame(['Random forest', train_accuracy, test_accuracy]).transpose()
#             rf_results.columns = ['Method', 'Training Accuracy', 'Test Accuracy']
#             # Convert objects to numerics
#             for col in rf_results.columns:
#                 rf_results[col] = pd.to_numeric(rf_results[col], errors='ignore')
#                 # Round to 3 digits
#                 rf_results = rf_results.round(3)

#         status.update(label="Status", state="complete", expanded=False)

#     # Display data info
#     st.header('Input data', divider='rainbow')
#     col = st.columns(4)
#     col[0].metric(label="No. of samples", value=X.shape[0], delta="")
#     col[1].metric(label="No. of X variables", value=X.shape[1], delta="")
#     col[2].metric(label="No. of Training samples", value=X_train.shape[0], delta="")
#     col[3].metric(label="No. of Test samples", value=X_test.shape[0], delta="")

#     # Zip dataset files
#     df.to_csv('dataset.csv', index=False)
#     X_train.to_csv('X_train.csv', index=False)
#     y_train.to_csv('y_train.csv', index=False)
#     X_test.to_csv('X_test.csv', index=False)
#     y_test.to_csv('y_test.csv', index=False)
#     y_train_pred_df = pd.DataFrame(y_train_pred)
#     y_test_pred_df = pd.DataFrame(y_test_pred)
#     y_train_pred_df.to_csv('pred_train.csv', index=False)
#     y_test_pred_df.to_csv('pred_test.csv', index=False)

#     list_files = ['dataset.csv', 'X_train.csv', 'y_train.csv', 'X_test.csv', 'y_test.csv', 'pred_train.csv', 'pred_test.csv']
#     with zipfile.ZipFile('dataset.zip', 'w') as zipF:
#         for file in list_files:
#             zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)

#     with open('dataset.zip', 'rb') as datazip:
#         btn = st.download_button(
#                 label='Download ZIP',
#                 data=datazip,
#                 file_name="dataset.zip",
#                 mime="application/octet-stream"
#                 )

#     # Display model parameters
#     st.header('Model parameters', divider='rainbow')
#     parameters_col = st.columns(2)
#     parameters_col[0].metric(label="Data split ratio (% for Training Set)", value=parameter_split_size, delta="")
#     parameters_col[1].metric(label="Number of estimators (n_estimators)", value=parameter_n_estimators, delta="")
#     #parameters_col[2].metric(label="Max features (max_features)", value=parameter_max_features_metric, delta="")

#     # Display feature importance plot
#     importances = rf.feature_importances_
#     feature_names = list(X_combined.columns)
#     forest_importances = pd.Series(importances, index=feature_names)
#     df_importance = forest_importances.reset_index().rename(columns={'index': 'feature', 0: 'value'})

#     bars = alt.Chart(df_importance).mark_bar(size=40).encode(
#                 x='value:Q',
#                 y=alt.Y('feature:N', sort='-x')
#             ).properties(height=250)

#     if problem_type != "Regression":
#         performance_col = st.columns((2, 0.2, 3))
#         with performance_col[0]:
#             st.header('Model performance', divider='rainbow')
#             st.dataframe(rf_results.T.reset_index().rename(columns={'index': 'Parameter', 0: 'Value'}))
#         with performance_col[2]:
#             st.header('Feature importance', divider='rainbow')
#             st.altair_chart(bars, theme='streamlit', use_container_width=True)
#     else:
#         st.header('Feature importance', divider='rainbow')
#         st.altair_chart(bars, theme='streamlit', use_container_width=True)

#     st.header('SHAP Analysis', divider='rainbow')

#     # Fit SHAP explainer to the trained Random Forest model
#     explainer = shap.Explainer(rf, X_train)

#     # Calculate SHAP values for the test set
#     shap_values = explainer(X_test, check_additivity=False)

#     # Summary plot of SHAP values
#     st.subheader('SHAP Summary Plot')
#     with st.spinner('Generating SHAP summary plot...'):
#         shap.plots.beeswarm(shap_values, max_display = 20, show=False)
#         st.pyplot(bbox_inches='tight')
#         st.write("The summary plot shows the average impact of each feature on the model's predictions and its direction.")

#     # SHAP dependence plot for a specific feature (e.g., the most important feature)
#     st.subheader('SHAP Dependence Plot')
#     with st.spinner('Generating SHAP dependence plot...'):
        
#         # Identify one-hot encoded features
#         # Assuming one-hot encoded features have a common prefix like 'cat_' or 'feature_'
#         one_hot_features = [col for col in X_test.columns if any(col.startswith(prefix) for prefix in categorical_cols)]

#         # Get all numerical features (which includes both continuous and one-hot)
#         numerical_features = X_test.select_dtypes(include=[np.number]).columns.tolist()

#         # Identify continuous features from the original list that are still in the DataFrame
#         continuous_features = [feature for feature in numerical_features if feature not in one_hot_features]
        
#         # Get absolute SHAP values
#         abs_shap_values = np.abs(shap_values.values)

#         # If continuous features exist, get the most important one
#         if len(continuous_features) > 0:
#             most_important_continuous_feature_index = np.argmax(abs_shap_values[:, X.columns.get_indexer(continuous_features)].mean(axis=0))
#             most_important_feature = continuous_features[most_important_continuous_feature_index]
#         else:
#             # Otherwise, get the overall most important feature
#             most_important_feature = X_test.columns[np.abs(shap_values.values).mean(axis=0).argmax()]
#         sample_ind = 20
#         shap.partial_dependence_plot(
#             most_important_feature,
#             rf.predict,
#             X_train,
#             model_expected_value=True,
#             feature_expected_value=True,
#             show=False,
#             ice=False,
#         )
#         st.pyplot(bbox_inches='tight')
#         st.write(f"The dependence plot shows how the feature `{most_important_feature}` affects the model's predictions.")

#     # Force plot for a single prediction
#     st.subheader('SHAP Force Plot')
#     with st.spinner('Generating SHAP force plot...'):
#         # Choose an index for a specific prediction (e.g., the first prediction)
#         shap.force_plot(
#             explainer.expected_value, shap_values.values[0, :], X_test.iloc[0, :], feature_names=X_test.columns, show=False, matplotlib=True
#         )
#         st.pyplot(bbox_inches='tight')
#         st.write("The force plot shows the contribution of each feature to a single prediction.")

#     if gam_data is True:
#         categorical_cols = df_gam.select_dtypes(include=['object', 'category']).columns
#         X_gam_encoded = one_hot_encoder.fit_transform(df_gam[categorical_cols])

#         # Convert the one-hot encoded columns to a DataFrame and combine with the remaining columns
#         X_gam_encoded_df = pd.DataFrame(X_gam_encoded.toarray(), columns=one_hot_encoder.get_feature_names_out(categorical_cols))
#         X_gam_combined = pd.concat([X_gam_encoded_df, df_gam.drop(columns=categorical_cols).reset_index(drop=True)], axis=1)

#         # Identify columns that are common to both dataframes
#         common_columns = X_combined.columns.intersection(X_gam_combined.columns)

#         # Select only these columns from the second dataframe
#         X_gam_combined_filtered = X_gam_combined[common_columns]

#         # Identify columns that are in df1 but not in df2
#         missing_columns = X_combined.columns.difference(X_gam_combined.columns)

#         # Add missing columns to df2 and fill with zeros
#         for col in missing_columns:
#             X_gam_combined_filtered[col] = 0

#         # Reorder the columns to match the order in df1
#         X_gam_combined_final = X_gam_combined_filtered[X_combined.columns]

#         y_gam_pred = rf.predict(X_gam_combined_final)
#         df_y_gam_pred = pd.DataFrame(y_gam_pred, columns=['Prev'])
        
#         @st.cache_data
#         def convert_df(df):
#             # IMPORTANT: Cache the conversion to prevent computation on every rerun
#             return df.to_csv().encode("utf-8")
#         csv = convert_df(df_y_gam_pred)

#         st.download_button(
#             label="Download predictions",
#             data=csv,
#             file_name="my_predictions.csv",
#             mime="text/csv",
#         )
        
# # Ask for CSV upload if none is detected
# else:
#     st.warning('👈 Upload a CSV file or click *"Load example data"* to get started!')

