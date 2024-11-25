import streamlit as st
import pandas as pd

def sidebar_config(i):
    with st.sidebar:
        if i == 0:
            # Load data
            st.header('Input data')

            col_sep = st.selectbox(
                'What is the column separator of your file:',
                [',',';']
            )
            dec_id = st.selectbox(
                'What is the decimal point character:',
                ['.',',']
            )

            uploaded_file = st.file_uploader("Upload the training set", type=["csv"])
            if uploaded_file is not None:
                st.session_state.uploaded  = True
                st.session_state.df_original = pd.read_csv(uploaded_file, sep=col_sep, index_col=False, decimal=dec_id)

            #Revise in the end
            #gam_data = st.toggle('Export Predictions')
            #if gam_data is True:
            #    gam_file = st.file_uploader("Upload the data to predict", type=["csv"])
            #    if gam_file is not None:
            #        df_gam = pd.read_csv(gam_file, sep=';', index_col=False)

        elif i == 1:
            # Select variables to analyze in detail
            st.header('Variable selection')
            var_1 = st.selectbox(
                'Select a variable to analyze in detail:',
                st.session_state.df_original.columns
            )
            st.session_state.var_1 = var_1

            var_2 = st.selectbox(
                'Select a second variable to analyze in detail:',
                list(set(st.session_state.df_original.columns) - {var_1})
            )
            st.session_state.var_2 = var_2

        elif i == 2:
            st.header('Data preparation')
            st.write('Categorical data')
            categorical_treat = st.selectbox(
                'How to treat categorical data:',
                ['Remove columns', 'Label encoding', 'One-hot encoding'] #Add target encoding in the future
            )
            st.session_state.categorical_treat = categorical_treat

            st.write('Missing values treatment')
            missing_treat = st.selectbox(
                'How to treat missing values:',
                ['Remove observation', 'Imputation: mean', 'Imputation: median'] 
            )
            st.session_state.missing_treat = missing_treat

            #Add option of how to find outliers
            st.write('Outlier treatment')
            outlier_treat = st.selectbox(
                'How to treat outlier values:',
                ['Keep as-is', 'Remove observation', 'Imputation: mean', 'Imputation: median'] 
            )
            st.session_state.outlier_treat = outlier_treat

        elif i == 3:

            st.header('Problem Type')
            problem_type = st.sidebar.radio('Choose problem type:', ['Regression', 'Classification'])
            st.session_state.problem_type = problem_type

            st.header('Variable selection')
            to_predict = st.selectbox(
                'Select the variable you want to predict:',
                st.session_state.df_treated.columns
            )
            st.session_state.to_predict = to_predict
            
            input_variables = st.multiselect(
                'Select the input variables you want to use:', 
                list(set(st.session_state.df_treated.columns) - {to_predict}),
                default=list(set(st.session_state.df_treated.columns) - {to_predict})
            )
            st.session_state.input_variables = input_variables

            st.header('Training Parameters')
            parameter_split_size = st.slider('Data split ratio (% for Training Set)', 10, 90, 80, 5)
            st.session_state.parameter_split_size = parameter_split_size

            st.header('Model Parameters')
            st.subheader('Machine learning model')
            if problem_type == 'Regression':
                model_to_use = st.sidebar.radio('Choose model:', ['Linear regression', 'Random forest', 'Gradient boosting machines'])
            else:
                model_to_use = st.sidebar.radio('Choose model:', ['Logistic regression', 'Random forest', 'Gradient boosting machines'])
            st.session_state.model_to_use = model_to_use

            st.subheader('Learning Parameters')
            #if model_to_use == 'Linear regression':
                # No additional parameters
            
            if model_to_use == 'Logistic regression':
                st.session_state.parameter_penalty = st.sidebar.radio(
                    'Penalty type (penalty)', ['l2', 'none'])
                st.session_state.parameter_c_value = st.sidebar.slider(
                    'Regularization strength (C)', 0.01, 10.0, 1.0, 0.01)
                st.session_state.parameter_solver = st.sidebar.radio(
                    'Solver', ['lbfgs', 'saga', 'liblinear'])
            
            if st.session_state.model_to_use in ['Random forest', 'Gradient boosting machines']:
                st.session_state.parameter_n_estimators = st.sidebar.slider(
                    'Number of estimators (n_estimators)', 5, 500, 100, 5)
                
                if st.session_state.model_to_use == 'Gradient boosting machines':
                    st.session_state.parameter_learning_rate = st.sidebar.slider(
                        'Learning rate', 0.01, 1.0, 0.1, 0.01)
                
                st.session_state.parameter_max_depth = st.sidebar.slider(
                    'Maximum depth of trees (max_depth)', 1, 100, 10, 1)
                
                st.session_state.parameter_min_samples_split = st.sidebar.slider(
                    'Minimum samples to split a node (min_samples_split)', 2, 20, 2, 1)
                
                st.session_state.parameter_min_samples_leaf = st.sidebar.slider(
                    'Minimum samples in leaf node (min_samples_leaf)', 1, 20, 1, 1)
                
                if st.session_state.problem_type == 'Regression':
                    if st.session_state.model_to_use == 'Random forest':
                        st.session_state.parameter_criterion = st.sidebar.radio(
                            'Performance measure (criterion)', 
                            ['squared_error', 'absolute_error', 'poisson', 'friedman_mse']
                        )
                    elif st.session_state.model_to_use == 'Gradient boosting machines':
                        st.session_state.parameter_criterion = st.sidebar.radio(
                            'Loss function (loss)', 
                            ['squared_error', 'absolute_error', 'huber', 'quantile']
                        )

                elif st.session_state.problem_type == 'Classification':
                    if st.session_state.model_to_use == 'Random forest':
                        st.session_state.parameter_criterion = st.sidebar.radio(
                            'Performance measure (criterion)', 
                            ['gini', 'entropy', 'log_loss']
                        )
                    elif st.session_state.model_to_use == 'Gradient boosting machines':
                        st.session_state.parameter_criterion = st.sidebar.radio(
                            'Loss function (loss)', 
                            ['log_loss', 'exponential']
                        )
                    st.session_state.balance_strat = st.sidebar.radio(
                            'Balancing strategy', 
                            ['None', 'Balance']
                        )

                #parameter_bootstrap = st.select_slider('Bootstrap samples when building trees (bootstrap)', options=[True, False])
                #parameter_oob_score = st.select_slider('Whether to use out-of-bag samples to estimate the R^2 on unseen data (oob_score)', options=[False, True])

            st.header('Other Parameters')
            st.session_state.parameter_random_state = st.slider('Seed number (random_state)', 0, 1000, 42, 1)

        elif i == 4:
            st.header('Result Parameters')
            st.subheader('Metric analysis')
            if st.session_state.problem_type == 'Regression':
                st.session_state.mae_analysis = st.sidebar.radio('Compare Mean Absolute Error (MAE):', ['Yes', 'No'])
                st.session_state.mse_analysis = st.sidebar.radio('Compare Mean Squared Error (MSE):', ['Yes', 'No'])
                st.session_state.rmse_analysis = st.sidebar.radio('Compare Root Mean Squared Error (RMSE):', ['Yes', 'No'])
                st.session_state.r2_analysis = st.sidebar.radio('Compare R² Score:', ['Yes', 'No'])
                st.session_state.evs_analysis = st.sidebar.radio('Compare Explained Variance Score:', ['Yes', 'No'])

            else:
                st.session_state.conf_analysis = st.sidebar.radio('Analyze Confusion Matrix:', ['Yes', 'No'])
                st.session_state.accuracy_analysis = st.sidebar.radio('Compare Accuracy:', ['Yes', 'No'])
                st.session_state.precision_analysis = st.sidebar.radio('Compare Precision:', ['Yes', 'No'])
                st.session_state.recall_analysis = st.sidebar.radio('Compare Recall:', ['Yes', 'No'])
                st.session_state.f1_analysis = st.sidebar.radio('Compare F1 Score:', ['Yes', 'No'])
                st.session_state.auc_analysis = st.sidebar.radio('Analyze ROC AUC:', ['Yes', 'No'])
                st.session_state.logloss_analysis = st.sidebar.radio('Compare Log Loss:', ['Yes', 'No'])
        
        elif i == 5:
            st.header('Model interpretation')
            st.subheader('Analysis parameters')
            if st.session_state.model_to_use in ['Random forest', 'Gradient boosting machines']:
                st.session_state.var_analysis = st.selectbox(
                    'Select a variable to analyze in detail:',
                    st.session_state.x_train.columns
                )
                
        elif i == 6:
            st.header('Prediction data')

            col_sep = st.selectbox(
                'What is the column separator of your file:',
                [',',';']
            )
            dec_id = st.selectbox(
                'What is the decimal point character:',
                ['.',',']
            )

            uploaded_file_output = st.file_uploader("Upload the training set", type=["csv"])
            if uploaded_file_output is not None:
                st.session_state.predict_output  = True
                st.session_state.df_to_predict = pd.read_csv(uploaded_file_output, sep=col_sep, index_col=False, decimal=dec_id)

            st.session_state.download_everything = st.selectbox(
                'Do you want to download the training and test set:',
                ['Yes','No'],
                index=1
            )