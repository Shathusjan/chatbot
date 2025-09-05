from typing import Dict, Optional
from features.quote_fields import QUOTE_FIELDS, VALIDATORS
from features.email_utils import send_quotation_email

def send_quote_email(quote_data: Dict[str, str]) -> None:
    """
    Stub for sending quote details via email.
    In production, this would send an email to the business.
    """
    # Here you would integrate with your email sending logic.
    # For now, we just print (or pass)
    print("Sending quote email with data:", quote_data)

def handle_quote_flow(user_input: str, session: dict) -> tuple:
    """
    Manages the quote conversation flow.
    Args:
        user_input: The latest user message.
        session: A dict-like object storing session state.
    Returns:
        A tuple (reply, options) to send to the user.
    """
    # Initialize session state if not present
    if "quote_step" not in session:
        session["quote_step"] = 0
        session["quote_data"] = {}
        session["quote_in_progress"] = True

    step = session["quote_step"]
    quote_data = session["quote_data"]

    if step == 0:
        session["quote_step"] = 1
        question = QUOTE_FIELDS[0][1]
        field_name = QUOTE_FIELDS[0][0]
        options = QUOTE_FIELDS[0][2] if len(QUOTE_FIELDS[0]) > 2 else []
        if options:
            return question, options
        else:
            return question, []

    # Save previous user input to the last field asked, except for the first step where no input yet
    if step > 0 and step <= len(QUOTE_FIELDS):
        field_def = QUOTE_FIELDS[step - 1]
        field_name = field_def[0]
        question = field_def[1]
        options = field_def[2] if len(field_def) > 2 else []
        validator = VALIDATORS.get(field_name)
        input_value = user_input.strip()
        if validator and not validator(input_value):
            # Input invalid, re-ask the same question with error message
            error_message = f"Invalid input for {field_name}. Please try again."
            if options:
                return f"{error_message}\n{question}", options
            else:
                return f"{error_message}\n{question}", []

        quote_data[field_name] = input_value

    # If all fields have been collected, generate summary, send email, reset session and return summary
    if step >= len(QUOTE_FIELDS):
        send_quote_email(quote_data)
        summary_lines = ["Thank you for your request! Here is the information you provided:"]
        for field_def in QUOTE_FIELDS:
            field_name = field_def[0]
            summary_lines.append(f"{field_name.capitalize()}: {quote_data.get(field_name, '')}")
        # Send summary as email to the user
        user_email = quote_data.get("email", "")
        confirmation_message = ""
        if user_email:
            try:
                send_quotation_email(user_email, "\n".join(summary_lines))
                confirmation_message = f"\n✅ Your quotation has been emailed to {user_email}. Please check your inbox."
            except Exception:
                confirmation_message = "⚠️ Something went wrong sending the email. Please try again later."
        summary_lines.append(confirmation_message)
        summary_message = "\n".join(summary_lines)
        # Reset session state for quote flow
        session.pop("quote_step", None)
        session.pop("quote_data", None)
        session["quote_in_progress"] = False
        return summary_message, []

    # Otherwise, ask the next question
    next_field_def = QUOTE_FIELDS[step]
    next_field_prompt = next_field_def[1]
    options = next_field_def[2] if len(next_field_def) > 2 else []
    session["quote_step"] = step + 1
    if options:
        return next_field_prompt, options
    else:
        return next_field_prompt, []