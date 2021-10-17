data1 = {
    "passcode": "1234",
    "timezone_name": "America/New_York",
    "pills": [
        {
            "slot": 1,
            "name": "Vitamin C",
            "dosage": "200 mg",
            "expires": "2020-03-14",
            "passcode_required": "true",
            "form": "Cap",
            "exact_pill_count": 10,
            "max_manual_doses": 3
        },
        {
            "slot": 2,
            "name": "Vitamin D",
            "dosage": "100 mg",
            "expires": "2020-03-14",
            "passcode_required": "false",
            "form": "Cap",
            "exact_pill_count": 22,
            "max_manual_doses": 1
        },
        {
            "slot": 3,
            "name": "Vitamin A",
            "dosage": "200 mg",
            "expires": "2020-03-14",
            "passcode_required": "false",
            "form": "Cap",
            "exact_pill_count": 22,
            "max_manual_doses": 1
        }
    ]
}

data2 = {
    "Table": {
        "device": {
            "passcode": "1234",
            "timezone_name": "America/New_York"
        },
        "consumables": [
            {
                "id": "id_1",
                "name": "Vitamin C",
                "expiration_date": "2020-03-14",
                "dosage": "200 mg",
                "passcode_mandatory": "false",
                "form": "Cap",
                "max_doses": 4
            },
            {
                "id": "id_2",
                "name": "Vitamin D",
                "expiration_date": "2020-03-14",
                "dosage": "200 mg",
                "passcode_mandatory": "false",
                "form": "Cap",
                "max_doses": 4
            }
        ],
        "slots": [
            {
                "slot_index": 1,
                "consumable_id": "id_1",
                "exact_pill_count": 21
            },
            {
                "slot_index": 2,
                "consumable_id": "id_2",
                "exact_pill_count": 20
            }
        ]
    }
}