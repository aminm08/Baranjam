from invitations.models import Invitation


def inbox(request):
    invitations = None
    if request.user.is_authenticated:
        invitations = Invitation.objects.filter(user_receiver=request.user)
    return {'inbox': invitations}
