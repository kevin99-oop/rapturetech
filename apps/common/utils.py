from .models import DPU, Customer

def get_user_st_id(user):
    # Replace this with the actual logic to get the user's ST_ID and range from CSV
    # You may retrieve it from the user's profile or any other related model
    # For example, assuming the user's profile has an 'st_id' field:

    if user.is_authenticated:
        try:
            dpu = DPU.objects.get(user=user)
            st_id = dpu.st_id

            # Get the corresponding CSV data for the user
            customer = Customer.objects.get(user=user, st_id=st_id)
            start_range = customer.start_range
            end_range = customer.end_range

            return st_id, start_range, end_range
        except (DPU.DoesNotExist, Customer.DoesNotExist):
            return None, None, None
    else:
        return None, None, None
