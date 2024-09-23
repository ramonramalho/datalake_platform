from operator_strategy import *

class OperatorFactory:
    """Fábrica para criar operadores com a estratégia apropriada."""
    
    strategies = {
        "EMRServerlessOperator": EMRServerlessOperator(),
    }
    
    @staticmethod
    def get_strategy(operator_type):
        """Retorna a estratégia apropriada com base no tipo do operador."""
        strategy = OperatorFactory.strategies.get(operator_type)
        if not strategy:
            raise ValueError(f"Unsupported operator type: {operator_type}")
        return strategy
