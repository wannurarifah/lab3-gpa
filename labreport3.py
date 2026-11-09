
import streamlit as st
import json

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Scholarship Advisory System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Scholarship Advisory System")
st.write("Rule-Based Decision Support System for Scholarship Applicants")

st.divider()

# ==========================================
# 2. DEFAULT SCHOLARSHIP RULES
# ==========================================

default_rules = [
    {
        "name": "Top merit candidate",
        "priority": 100,
        "conditions": [
            ["cgpa", ">=", 3.7],
            ["co_curricular_score", ">=", 80],
            ["family_income", "<=", 8000],
            ["disciplinary_actions", "==", 0]
        ],
        "action": {
            "decision": "AWARD_FULL",
            "reason": "Excellent academic & co-curricular performance, with acceptable need"
        }
    },
    {
        "name": "Good candidate - partial scholarship",
        "priority": 80,
        "conditions": [
            ["cgpa", ">=", 3.3],
            ["co_curricular_score", ">=", 60],
            ["family_income", "<=", 12000],
            ["disciplinary_actions", "<=", 1]
        ],
        "action": {
            "decision": "AWARD_PARTIAL",
            "reason": "Good academic & involvement record with moderate need"
        }
    },
    {
        "name": "Need-based review",
        "priority": 70,
        "conditions": [
            ["cgpa", ">=", 2.5],
            ["family_income", "<=", 4000]
        ],
        "action": {
            "decision": "REVIEW",
            "reason": "High need but borderline academic score"
        }
    },
    {
        "name": "Low CGPA – not eligible",
        "priority": 95,
        "conditions": [
            ["cgpa", "<", 2.5]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "CGPA below minimum scholarship requirement"
        }
    },
    {
        "name": "Serious disciplinary record",
        "priority": 90,
        "conditions": [
            ["disciplinary_actions", ">=", 2]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "Too many disciplinary records"
        }
    }
]

# ==========================================
# 3. RULE ENGINE
# ==========================================

def check_condition(facts, condition):

    attribute = condition[0]
    operator = condition[1]
    threshold = condition[2]

    value = facts[attribute]

    if operator == ">=":
        return value >= threshold

    elif operator == "<=":
        return value <= threshold

    elif operator == ">":
        return value > threshold

    elif operator == "<":
        return value < threshold

    elif operator == "==":
        return value == threshold

    elif operator == "!=":
        return value != threshold

    else:
        raise ValueError("Invalid operator: " + operator)


def evaluate_rules(facts, rules):

    matched_rules = []

    for rule in rules:

        results = []

        for condition in rule["conditions"]:

            result = check_condition(facts, condition)

            results.append(result)

        # All conditions must be TRUE
        if all(results):
            matched_rules.append(rule)

    # Select rule with highest priority
    if len(matched_rules) > 0:

        matched_rules.sort(
            key=lambda x: x["priority"],
            reverse=True
        )

        return matched_rules[0], matched_rules

    return None, matched_rules


# ==========================================
# 4. APPLICANT INFORMATION
# ==========================================

st.header("1. Applicant Information")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input("Applicant Name")

    cgpa = st.number_input(
        "Cumulative GPA (CGPA)",
        min_value=0.0,
        max_value=4.0,
        value=3.50,
        step=0.01
    )

    family_income = st.number_input(
        "Monthly Family Income (RM)",
        min_value=0,
        value=3000,
        step=100
    )

    co_curricular_score = st.number_input(
        "Co-curricular Involvement Score",
        min_value=0,
        max_value=100,
        value=75
    )

with col2:

    community_hours = st.number_input(
        "Community Service Hours",
        min_value=0,
        value=20
    )

    semester = st.number_input(
        "Current Semester",
        min_value=1,
        max_value=12,
        value=4
    )

    disciplinary_actions = st.number_input(
        "Number of Disciplinary Actions",
        min_value=0,
        value=0
    )


st.divider()

# ==========================================
# 5. JSON RULE CONFIGURATION
# ==========================================

st.header("2. Rule Configuration")

st.write(
    "Edit the JSON rules below to change "
    "the scholarship eligibility criteria."
)

json_text = st.text_area(
    "JSON Rule Editor",
    value=json.dumps(default_rules, indent=2),
    height=450
)


st.divider()

# ==========================================
# 6. SCHOLARSHIP EVALUATION
# ==========================================

st.header("3. Scholarship Evaluation")

if st.button("Evaluate Scholarship Application", type="primary"):

    try:

        # Check applicant name
        if name.strip() == "":
            st.error("Please enter the applicant name.")

        else:

            # Read JSON rules
            rules = json.loads(json_text)

            if not isinstance(rules, list) or len(rules) == 0:
                raise ValueError("Rules must be a non-empty JSON list.")

            # Store applicant information as facts
            facts = {
                "cgpa": cgpa,
                "family_income": family_income,
                "co_curricular_score": co_curricular_score,
                "community_hours": community_hours,
                "semester": semester,
                "disciplinary_actions": disciplinary_actions
            }

            # Evaluate all rules
            selected_rule, matched_rules = evaluate_rules(
                facts, rules
            )

            st.divider()

            st.subheader("Evaluation Result")

            st.write("**Applicant Name:**", name)

            if selected_rule is not None:

                decision = selected_rule["action"]["decision"]

                reason = selected_rule["action"]["reason"]

                st.success("Decision: " + decision)

                st.write(
                    "**Selected Rule:**",
                    selected_rule["name"]
                )

                st.write(
                    "**Priority:**",
                    selected_rule["priority"]
                )

                st.write(
                    "**Reason:**",
                    reason
                )

                st.subheader("Matching Rules")

                for rule in matched_rules:

                    st.write(
                        "•",
                        rule["name"],
                        "| Priority:",
                        rule["priority"]
                    )

            else:

                st.warning(
                    "NO AWARD - No scholarship rules were matched."
                )

                st.write(
                    "The applicant does not satisfy "
                    "any predefined scholarship criteria."
                )

    except json.JSONDecodeError:

        st.error("Invalid JSON format. Please check your rules.")

    except (ValueError, KeyError, TypeError, IndexError) as error:

        st.error("Evaluation error: " + str(error))


# ==========================================
# 7. FOOTER
# ==========================================

st.divider()

st.caption(
    "Scholarship Advisory System | "
    "Python + Streamlit | Rule-Based AI"
)