from .views import PropertyView,ClosedView, PayPropView, ClosedProp, InterestProp, ContractProp, FundedProp, OwnedPropView,ContractView, TrendingProp, DetailView, GetProps, ProposedView, InterestsView, FundedView
from django.urls import path


urlpatterns = [
    path('properties', PropertyView.as_view()),
    path('property', OwnedPropView.as_view()),
    path('trend', TrendingProp.as_view()),
    path('detail', DetailView.as_view()),
    path('props', GetProps.as_view()),
    path('proposal', ProposedView.as_view()),
    path('interest',InterestsView.as_view() ),
    path('fund', FundedView.as_view() ),
    path('contract', ContractView.as_view()),
    path('close', ClosedView.as_view()),
    path('interested', InterestProp.as_view()),
    path('funded', FundedProp.as_view()),
    path('closed', ClosedProp.as_view()),
    path('contracted', ContractProp.as_view() ),
    path('buy', PayPropView.as_view())
]

