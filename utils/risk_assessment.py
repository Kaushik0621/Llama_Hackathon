def assess_risk(responses):
    total_score = 0

    # Question 1
    q1 = responses.get('question1')
    if q1 == 'Severe chest pain or difficulty breathing':
        total_score += 10
    elif q1 == 'Uncontrolled bleeding or loss of consciousness':
        total_score += 10
    elif q1 == 'Severe pain (e.g., abdominal, head)':
        total_score += 7
    elif q1 == 'Fever, cough, or mild pain':
        total_score += 4
    elif q1 == 'No significant symptoms, general check-up':
        total_score += 1

    # Question 2
    q2 = responses.get('question2')
    if q2 == 'Less than 1 hour':
        total_score += 8
    elif q2 == '1–24 hours':
        total_score += 5
    elif q2 == '1–7 days':
        total_score += 3
    elif q2 == 'More than a week':
        total_score += 1

    # Question 3 (Select all that apply)
    q3_options = responses.get('question3', [])
    if isinstance(q3_options, str):  # Handle single value (non-multi-select)
        q3_options = [q3_options]
    for option in q3_options:
        if option == 'Dizziness or confusion':
            total_score += 7
        elif option == 'Severe weakness or inability to move':
            total_score += 6
        elif option == 'Nausea/vomiting that doesn’t stop':
            total_score += 5
        elif option == 'Moderate fatigue or discomfort':
            total_score += 3
        elif option == 'None of the above':
            total_score += 0

    # Question 4
    q4 = responses.get('question4')
    if q4 == 'Heart disease, diabetes, or immunocompromised conditions':
        total_score += 5
    elif q4 == 'Pregnant or recent surgery (past 4 weeks)':
        total_score += 5
    elif q4 == 'None':
        total_score += 0

    # Question 5
    q5 = responses.get('question5')
    if q5 == 'Head injury or severe trauma':
        total_score += 8
    elif q5 == 'Moderate injury or significant pain':
        total_score += 5
    elif q5 == 'Minor cuts, bruises, or sprains':
        total_score += 2
    elif q5 == 'No injuries':
        total_score += 0

    # Determine risk level
    if total_score >= 20:
        risk_level = 'Red'
    elif 10 <= total_score < 20:
        risk_level = 'Yellow'
    else:
        risk_level = 'Green'

    return risk_level, total_score
