import streamlit as st
import joblib
from datetime import date


# Load trained model and its metadata
model = joblib.load('model/finalModel.joblib')
feature_scaler = joblib.load('model/featureScaler.joblib')
target_scaler = joblib.load('model/targetScaler.joblib')


def app():
    st.title('Transfer Fee Predictor')

    st.markdown('This app is designed to predict the transfer fee of a'
                ' footballer (soccer player) given his market value, hypothetical date of transfer,'
                ' and the expiry date of his current contract')

    # Obtain Market Value
    market_value = st.number_input('Market Value in Millions of Euros (€):',
                                   min_value=10, max_value=300)
    mv = market_value * 1000000

    col1, col2 = st.columns(2)

    with col1:
        # Obtain hypothetical date of transfer
        transfer_date = st.date_input('Date of Transfer', min_value=date.today())

    with col2:
        # Obtain contract expiry date
        end_date = st.date_input('Contract Expiry Date', min_value=date.today())

    days_remaining = (end_date - transfer_date).days

    # Predict using model
    if st.button('Predict'):
        # Feature Scaling
        X = feature_scaler.transform([[mv, days_remaining]])

        # Inverse Scaling
        model_pred = model.predict(X).reshape(-1, 1)
        scaled_pred = target_scaler.inverse_transform(model_pred)

        # Formatting Output
        prediction = scaled_pred[0, 0]
        if abs(prediction) >= 1e9:
            formatted_prediction = "€{:.2f} B".format(prediction / 1e9)
        elif abs(prediction) >= 1e6:
            formatted_prediction = "€{:.2f} M".format(prediction / 1e6)
        elif abs(prediction) >= 1e3:
            formatted_prediction = "€{:.2f} K".format(prediction / 1e3)
        else:
            formatted_prediction = "€{:.2f}".format(prediction)

        st.success(f'Predicted Transfer Fee: {formatted_prediction}')


if __name__ == '__main__':
    app()
