# from geopy.distance import geodesic

from data_extraction import convert_dict_to_df, load_csv_and_convert_to_df
from datetime import datetime, timedelta

dataset = [
    {
        "transactionAmount": 1200,
        "dateTimeTransaction": 2412192200,
        "merchantCategoryCode": 5969,
        "cardBalance": 350000,
        "encryptedHexCardNo": "2a0d5647a9704ebb843c80cad064b8c3cdbfc2b15e5d35394a30fd4dfc945e67",
        "latitude": 28.644800,
        "longitude": 77.216721
    },
    {
        "transactionAmount": 1800,
        "dateTimeTransaction": 2412192200,
        "merchantCategoryCode": 5969,
        "cardBalance": 0000000000.00,
        "encryptedHexCardNo": "2a0d5647a9704ebb843c80cad064b8c3cdbfc2b15e5d35394a30fd4dfc945e67",
        "latitude": 28.644800,
        "longitude": 77.216721
    },
    {
        "transactionAmount": 1200,
        "dateTimeTransaction": 2412192200,
        "merchantCategoryCode": 5969,
        "cardBalance": 250000,
        "encryptedHexCardNo": "2a0d5647a9704ebb843c80cad064b8c3cdbfc2b15e5d35394a30fd4dfc945e67",
        "latitude": 28.644800,
        "longitude": 77.216721
    },
    {
        "transactionAmount": 7000,
        "dateTimeTransaction": 2412192200,
        "merchantCategoryCode": 5969,
        "cardBalance": 700000,
        "encryptedHexCardNo": "2a0d5647a9704ebb843c80cad064b8c3cdbfc2b15e5d35394a30fd4dfc945e67",
        "latitude": 28.644800,
        "longitude": 77.216721
    }
]


def calculate_distance(p1, p2):
    # p1 = (latitude, longitude)
    # p2 =  (latitude, longitude)
    return geodesic(p1, p2).kilometers


def rule_01(input_data, dataset, user_id=None):
    if user_id:
        dataset = dataset[dataset['encryptedPAN'].apply(
            lambda x: x == input_data['encryptedPAN'])]

    dataset = dataset[dataset['encryptedHexCardNo'].apply(
        lambda x: x == input_data['encryptedHexCardNo'])]
    twelve_hours_ago = datetime.fromtimestamp(input_data['dateTimeTransaction']) - \
        timedelta(hours=12)

    # filtered_df = dataset[dataset['dateTimeTransaction'].apply(
    #    lambda x: print(x))]
    filtered_df = dataset[dataset['dateTimeTransaction'].apply(
        lambda x: datetime.fromtimestamp(x/1000) >= twelve_hours_ago)]
    
    if (filtered_df.empty):
        return False
    
    filtered_df.sort_values(by='dateTimeTransaction')
    if not filtered_df.empty:
        card_balance = filtered_df.iloc[0]
        if card_balance >= 300000:
            if filtered_df['transactionAmount'].sum() >= 0.70*card_balance:
                return True
    return False


def rule_02(input_data, dataset, user_id=None):
    if user_id:
        dataset = dataset[dataset['encryptedPAN'].apply(
            lambda x: x == input_data['encryptedPAN'])]

    dataset = dataset[dataset['encryptedHexCardNo'].apply(
        lambda x: x == input_data['encryptedHexCardNo'])]
    twelve_hours_ago = datetime.fromtimestamp(input_data['dateTimeTransaction']) - \
        timedelta(hours=12)

    # filtered_df = dataset[dataset['dateTimeTransaction'].apply(
    #    lambda x: print(x))]
    filtered_df = dataset[dataset['dateTimeTransaction'].apply(
        lambda x: datetime.fromtimestamp(x/1000) >= twelve_hours_ago)]

    print(filtered_df)
    if (filtered_df.empty):
        return False

    if filtered_df['transactionAmount'].sum() >= 100000:
        count = 0
        for index, row in filtered_df.iterrows():
            distance = calculate_distance(
                (row['longitude'], row['latitude'], (input_data['longitude'], input_data['latitude'])))
            print(distance)
            if distance >= 200:
                count += 1
                if count > 5:
                    return True
    return False


def rule_03(input_data):
    pass


def detect(input_data):
    transaction_data = load_csv_and_convert_to_df('dataset/user_data.csv')
    violations = []
    if (rule_01(input_data, transaction_data)):
        violations.append("RULE-001")

    if (rule_02(input_data, transaction_data)):
        violations.append("RULE-002")

    return violations

input_data = {
    "transactionAmount": 300000,
    "dateTimeTransaction": 1712397351,
    "merchantCategoryCode": 5969,
    "cardBalance": 350000,
    "encryptedHexCardNo": "997ea24f732ed174be1eafd9e5834eb9838d09bc",
    "encryptedPAN": "Kg1WR6lwTruEPIDK0GS4w82/wrFeXTU5SjD9TfyUXmc=",
    "latitude": 28.644800,
    "longitude": 77.216721
}

# detect(input_data)
