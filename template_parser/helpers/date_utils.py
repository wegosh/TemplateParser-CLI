from dateutil.relativedelta import relativedelta

def apply_date_operations(date_obj, operations):
    delta_args = {}
    allowed_operations = [
        'add_years', 'subtract_years', 'add_months', 'subtract_months',
        'add_days', 'subtract_days', 'add_weeks', 'subtract_weeks',
        'add_hours', 'subtract_hours', 'add_minutes', 'subtract_minutes',
        'add_seconds', 'subtract_seconds'
    ]
    for op_name, value in operations.items():
        if op_name in allowed_operations:
            try:
                amount = int(value)
            except ValueError:
                raise ValueError(f"Invalid value for {op_name}: {value}. Must be an integer.")
            if 'subtract' in op_name:
                amount = -amount
            delta_key = op_name.replace('add_', '').replace('subtract_', '')
            delta_args[delta_key] = delta_args.get(delta_key, 0) + amount
    return date_obj + relativedelta(**delta_args)

