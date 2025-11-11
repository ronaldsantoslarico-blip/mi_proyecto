►# sistema_contador/modelos_ia.py
import numpy as np
from collections import defaultdict, Counter
from sklearn.ensemble import RandomForestClassifier

class CadenaMarkovPagos:
    """Sistema de predicción usando Cadenas de Markov"""
    
    def __init__(self):
        self.estados = ['al_dia', 'retraso_leve', 'retraso_grave', 'impago']
        self.matriz_transicion = None
        
    def entrenar(self, datos_historicos):
        """Entrenar la cadena de Markov con datos históricos"""
        if not datos_historicos:
            self._usar_matriz_default()
            return
        
        # Contar transiciones entre estados
        transiciones = defaultdict(Counter)
        
        for secuencia in datos_historicos:
            for i in range(len(secuencia) - 1):
                estado_actual = secuencia[i]
                estado_siguiente = secuencia[i + 1]
                transiciones[estado_actual][estado_siguiente] += 1
        
        # Construir matriz de transición
        self.matriz_transicion = {}
        for estado_actual in self.estados:
            total = sum(transiciones[estado_actual].values())
            if total > 0:
                self.matriz_transicion[estado_actual] = {
                    sig: count/total for sig, count in transiciones[estado_actual].items()
                }
            else:
                self.matriz_transicion[estado_actual] = self._probabilidades_default(estado_actual)
    
    def _usar_matriz_default(self):
        """Matriz de transición por defecto basada en conocimiento experto"""
        self.matriz_transicion = {
            'al_dia': {'al_dia': 0.7, 'retraso_leve': 0.2, 'retraso_grave': 0.08, 'impago': 0.02},
            'retraso_leve': {'al_dia': 0.3, 'retraso_leve': 0.4, 'retraso_grave': 0.2, 'impago': 0.1},
            'retraso_grave': {'al_dia': 0.1, 'retraso_leve': 0.2, 'retraso_grave': 0.4, 'impago': 0.3},
            'impago': {'al_dia': 0.05, 'retraso_leve': 0.15, 'retraso_grave': 0.3, 'impago': 0.5}
        }
    
    def _probabilidades_default(self, estado_actual):
        """Probabilidades por defecto para estados sin datos"""
        defaults = {
            'al_dia': {'al_dia': 0.7, 'retraso_leve': 0.2, 'retraso_grave': 0.08, 'impago': 0.02},
            'retraso_leve': {'al_dia': 0.3, 'retraso_leve': 0.4, 'retraso_grave': 0.2, 'impago': 0.1},
            'retraso_grave': {'al_dia': 0.1, 'retraso_leve': 0.2, 'retraso_grave': 0.4, 'impago': 0.3},
            'impago': {'al_dia': 0.05, 'retraso_leve': 0.15, 'retraso_grave': 0.3, 'impago': 0.5}
        }
        return defaults.get(estado_actual, {e: 0.25 for e in self.estados})
    
    def predecir(self, estado_actual, meses=3):
        """Predecir estados futuros"""
        if not self.matriz_transicion:
            self._usar_matriz_default()
        
        predicciones = []
        probabilidades = []
        estado = estado_actual
        
        for _ in range(meses):
            if estado in self.matriz_transicion:
                trans = self.matriz_transicion[estado]
                # Elegir estado más probable
                estado_sig = max(trans.items(), key=lambda x: x[1])
                predicciones.append(estado_sig[0])
                probabilidades.append(round(estado_sig[1] * 100, 2))
                estado = estado_sig[0]
            else:
                predicciones.append('al_dia')
                probabilidades.append(50.0)
        
        return predicciones, probabilidades
    
    def calcular_riesgo(self, estado_actual):
        """Calcular nivel de riesgo"""
        riesgo = {
            'al_dia': ('Bajo', 'success'),
            'retraso_leve': ('Moderado', 'warning'),
            'retraso_grave': ('Alto', 'orange'),
            'impago': ('Muy Alto', 'danger')
        }
        return riesgo.get(estado_actual, ('Desconocido', 'secondary'))

class PredictorML:
    """Predictor usando Machine Learning (Random Forest)"""
    
    def __init__(self):
        self.modelo = RandomForestClassifier(n_estimators=100, random_state=42)
        self.entrenado = False
    
    def entrenar(self, X, y):
        """Entrenar modelo con datos"""
        if len(X) > 0:
            self.modelo.fit(X, y)
            self.entrenado = True
            return self.modelo.score(X, y)
        return 0
    
    def predecir(self, X):
        """Realizar predicción"""
        if self.entrenado and len(X) > 0:
            proba = self.modelo.predict_proba(X)[0]
            return {
                'prob_pago': round(proba[0] * 100, 2),
                'prob_impago': round(proba[1] * 100, 2)
            }
        return {'prob_pago': 50.0, 'prob_impago': 50.0}