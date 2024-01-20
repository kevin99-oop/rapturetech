from apps.common.models import DPU


def get_user_st_id(user):
    try:
        dpu = DPU.objects.get(user=user)
        return dpu.st_id
    except DPU.DoesNotExist:
        return None