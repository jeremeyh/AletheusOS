from aletheus.oracle import bootstrap_oracle_service


def test_forecast():
 assert bootstrap_oracle_service().forecast().confidence>0
