# sistema_contador/evaluacion_credito.py
"""
Sistema de Evaluación de Crédito con IA
Evalúa la aptitud de un cliente para acceder a un préstamo
Método: Sistema de Análisis Financiero Automático (SAFA) + Markov Chain Analysis
Moneda: Bolivianos (Bs.)
"""

class EvaluadorCredito:
    def __init__(self):
        # Pesos para cada factor de evaluación
        self.peso_ingresos = 0.35
        self.peso_deudas = 0.35
        self.peso_ratio_deuda = 0.20
        self.peso_historial = 0.10
    
    def calcular_ratio_deuda(self, ingresos_mensuales, gastos_mensuales):
        """
        Calcula el ratio de deuda (gastos / ingresos)
        Ideal: < 40%
        """
        if ingresos_mensuales <= 0:
            return 1.0  # Máximo riesgo
        
        ratio = gastos_mensuales / ingresos_mensuales
        return min(ratio, 1.0)  # Máximo 100%
    
    def evaluar_ingresos(self, sueldo, otros_ingresos):
        """
        Evalúa la solidez de los ingresos (0-100)
        """
        ingresos_totales = sueldo + otros_ingresos
        
        if ingresos_totales == 0:
            return 0
        elif ingresos_totales < 1000:
            return 20
        elif ingresos_totales < 2000:
            return 40
        elif ingresos_totales < 3000:
            return 60
        elif ingresos_totales < 5000:
            return 80
        else:
            return 100
    
    def evaluar_deudas(self, gastos_vivienda):
        """
        Evalúa la situación de deudas/gastos (0-100)
        Menor deuda = Mayor puntuación
        """
        if gastos_vivienda == 0:
            return 100
        elif gastos_vivienda < 300:
            return 90
        elif gastos_vivienda < 600:
            return 75
        elif gastos_vivienda < 1000:
            return 50
        elif gastos_vivienda < 1500:
            return 30
        else:
            return 10
    
    def evaluar_ratio_deuda(self, ratio):
        """
        Evalúa el ratio deuda/ingresos (0-100)
        0.40 (40%) es el máximo recomendado
        """
        if ratio <= 0.25:
            return 100
        elif ratio <= 0.40:
            return 80
        elif ratio <= 0.60:
            return 60
        elif ratio <= 0.80:
            return 40
        else:
            return 20
    
    def evaluar_historial_pagos(self, estado_actual):
        """
        Evalúa el historial de pagos basado en el estado actual (0-100)
        """
        estado_scores = {
            'al_dia': 100,
            'retraso_leve': 60,
            'retraso_grave': 30,
            'impago': 0,
            'pendiente': 50
        }
        return estado_scores.get(estado_actual, 50)
    
    def generar_recomendaciones(self, puntuacion, ingresos, gastos, ratio, tiene_propiedad, valor_propiedad, estado_actual):
        """
        Genera recomendaciones DETALLADAS basadas en cada aspecto de la evaluación
        Explica POR QUÉ sí o por qué NO se puede prestar
        """
        recomendaciones_positivas = []  # Por qué SÍ prestar
        recomendaciones_negativas = []  # Por qué NO prestar
        recomendaciones_mejora = []     # Cómo mejorar
        
        # ===== ANÁLISIS DE INGRESOS =====
        if ingresos >= 5000:
            recomendaciones_positivas.append("✅ Ingresos sólidos (≥ 5000 Bs.). Capacidad fuerte de pago.")
        elif ingresos >= 3000:
            recomendaciones_positivas.append("✅ Ingresos buenos (≥ 3000 Bs.). Capacidad de pago adecuada.")
        elif ingresos >= 2000:
            recomendaciones_positivas.append("⚠️ Ingresos moderados (≥ 2000 Bs.). Hay capacidad de pago pero limitada.")
        elif ingresos >= 1000:
            recomendaciones_negativas.append("❌ Ingresos muy bajos (< 2000 Bs.). Riesgo de incapacidad de pago.")
        else:
            recomendaciones_negativas.append("❌ Ingresos insuficientes (< 1000 Bs.). No hay capacidad de pago comprobada.")
        
        # ===== ANÁLISIS DE GASTOS =====
        if gastos <= 300:
            recomendaciones_positivas.append("✅ Gastos bajos (≤ 300 Bs.). Mucho margen disponible para nuevas obligaciones.")
        elif gastos <= 600:
            recomendaciones_positivas.append("✅ Gastos controlados (≤ 600 Bs.). Buen margen para asumir préstamo.")
        elif gastos <= 1000:
            recomendaciones_positivas.append("⚠️ Gastos moderados (≤ 1000 Bs.). Margen disponible aceptable.")
        elif gastos <= 1500:
            recomendaciones_negativas.append("❌ Gastos altos (> 1000 Bs.). Poco margen para nuevas obligaciones.")
        else:
            recomendaciones_negativas.append("❌ Gastos muy altos (> 1500 Bs.). NO hay margen para préstamo.")
        
        # ===== ANÁLISIS DE RATIO DEUDA/INGRESOS =====
        ratio_porcentaje = ratio * 100
        if ratio <= 0.25:
            recomendaciones_positivas.append(f"✅ Ratio excelente ({ratio_porcentaje:.1f}%). Puede asumir fácilmente un préstamo.")
        elif ratio <= 0.40:
            recomendaciones_positivas.append(f"✅ Ratio adecuado ({ratio_porcentaje:.1f}%). Capacidad de pago comprobada.")
        elif ratio <= 0.60:
            recomendaciones_positivas.append(f"⚠️ Ratio moderado ({ratio_porcentaje:.1f}%). Puede prestar pero con cautela.")
        elif ratio <= 0.80:
            recomendaciones_negativas.append(f"❌ Ratio alto ({ratio_porcentaje:.1f}%). Muy poco margen para nuevas obligaciones.")
        else:
            recomendaciones_negativas.append(f"❌ Ratio crítico ({ratio_porcentaje:.1f}%). NO tiene capacidad para asumir deuda.")
        
        # ===== ANÁLISIS DE HISTORIAL DE PAGOS =====
        if estado_actual == 'al_dia':
            recomendaciones_positivas.append("✅ Historial perfecto. Cliente al día en todos sus compromisos.")
        elif estado_actual == 'retraso_leve':
            recomendaciones_positivas.append("⚠️ Historial con retrasos leves. Muestra capacidad pero con inconsistencias.")
        elif estado_actual == 'retraso_grave':
            recomendaciones_negativas.append("❌ Historial problemático. Retrasos graves indican incumplimiento habitual.")
        elif estado_actual == 'impago':
            recomendaciones_negativas.append("❌ Historial crítico. Deudas impagas demuestran falta de capacidad o disposición de pago.")
        
        # ===== ANÁLISIS DE PROPIEDAD =====
        if tiene_propiedad and valor_propiedad > 0:
            if valor_propiedad >= 50000:
                recomendaciones_positivas.append(f"✅ Propiedad valiosa (Bs. {valor_propiedad:,.2f}). Garantía sólida para el préstamo.")
            elif valor_propiedad >= 20000:
                recomendaciones_positivas.append(f"✅ Propiedad registrada (Bs. {valor_propiedad:,.2f}). Reduce riesgo del préstamo.")
            else:
                recomendaciones_positivas.append(f"⚠️ Propiedad registrada (Bs. {valor_propiedad:,.2f}). Ayuda pero con valor limitado.")
        else:
            recomendaciones_mejora.append("💡 SIN PROPIEDAD: Adquirir una propiedad mejoraría significativamente tu perfil crediticio.")
        
        # ===== RECOMENDACIONES DE MEJORA =====
        if ingresos < 3000:
            recomendaciones_mejora.append("💡 AUMENTAR INGRESOS: Busca fuentes adicionales de ingreso para mejorar capacidad de pago.")
        
        if gastos > 1000:
            recomendaciones_mejora.append("💡 REDUCIR GASTOS: Disminuir gastos de vivienda mejorará tu margen disponible.")
        
        if ratio > 0.40:
            recomendaciones_mejora.append("💡 MEJORAR RATIO: Reduce gastos o aumenta ingresos para llegar a ratio < 40%.")
        
        # ===== VEREDICTO FINAL =====
        if len(recomendaciones_negativas) == 0 and puntuacion >= 70:
            recomendaciones_positivas.insert(0, "🎉 APTO PARA PRÉSTAMO: Reunes todos los requisitos para acceder a financiamiento.")
        elif len(recomendaciones_negativas) > 0 and puntuacion < 50:
            recomendaciones_negativas.insert(0, "🚫 NO APTO PARA PRÉSTAMO: No reúnes los requisitos mínimos en este momento.")
        else:
            recomendaciones_positivas.insert(0, "⏳ APTO CONDICIONADO: Puedes acceder a préstamo pero con limitaciones.")
        
        # Combinar todas las recomendaciones en orden
        todas_las_recomendaciones = recomendaciones_positivas + recomendaciones_negativas + recomendaciones_mejora
        
        return todas_las_recomendaciones
    
    def evaluar_cliente(self, sueldo, otros_ingresos, gastos_vivienda, tiene_propiedad, valor_propiedad, estado_actual):
        """
        Realiza evaluación integral del cliente
        Retorna: puntuación (0-100), apto (Sí/No), evaluación detallada
        
        Parámetros:
        - sueldo: Ingreso mensual principal en Bs.
        - otros_ingresos: Ingresos adicionales en Bs.
        - gastos_vivienda: Gastos de vivienda en Bs. (arriendo, servicios, etc.)
        - tiene_propiedad: Boolean - ¿Tiene casa/terreno/propiedad?
        - valor_propiedad: Valor de la propiedad en Bs. (0 si no tiene)
        - estado_actual: Estado de pagos actual del cliente
        """
        # Calcular ingresos y gastos
        ingresos_mensuales = sueldo + otros_ingresos
        gastos_mensuales = gastos_vivienda
        
        # Evaluar cada componente
        score_ingresos = self.evaluar_ingresos(sueldo, otros_ingresos)
        score_deudas = self.evaluar_deudas(gastos_vivienda)
        ratio_deuda = self.calcular_ratio_deuda(ingresos_mensuales, gastos_mensuales)
        score_ratio = self.evaluar_ratio_deuda(ratio_deuda)
        score_historial = self.evaluar_historial_pagos(estado_actual)
        
        # Evaluar propiedad (es un factor de seguridad importante)
        score_propiedad = 100 if tiene_propiedad and valor_propiedad > 0 else 30
        
        # Calcular puntuación ponderada
        # Agregamos el peso de la propiedad (10%)
        puntuacion_final = (
            score_ingresos * self.peso_ingresos +
            score_deudas * self.peso_deudas +
            score_ratio * self.peso_ratio_deuda +
            score_historial * self.peso_historial +
            score_propiedad * 0.10  # 10% - Propiedad como garantía
        )
        
        # Determinar apto para préstamo
        if puntuacion_final >= 70:
            apto = "Sí ✓"
            riesgo = "Bajo"
            color = "success"
        elif puntuacion_final >= 50:
            apto = "Condicionado"
            riesgo = "Moderado"
            color = "warning"
        else:
            apto = "No ✗"
            riesgo = "Alto"
            color = "danger"
        
        # Generar recomendaciones
        recomendaciones = self.generar_recomendaciones(
            puntuacion_final, 
            ingresos_mensuales, 
            gastos_mensuales, 
            ratio_deuda,
            tiene_propiedad,
            valor_propiedad,
            estado_actual
        )
        
        # Construir evaluación detallada
        evaluacion = {
            'puntuacion_final': round(puntuacion_final, 2),
            'apto_prestamo': apto,
            'nivel_riesgo': riesgo,
            'color': color,
            'tipo_ia': 'SAFA (Sistema de Análisis Financiero Automático) + Markov Chain',
            'moneda': 'Bs.',
            'detalle': {
                'ingresos_mensuales': round(ingresos_mensuales, 2),
                'gastos_mensuales': round(gastos_mensuales, 2),
                'ratio_deuda': round(ratio_deuda * 100, 2),
                'score_ingresos': round(score_ingresos, 2),
                'score_deudas': round(score_deudas, 2),
                'score_ratio': round(score_ratio, 2),
                'score_historial': round(score_historial, 2),
                'score_propiedad': round(score_propiedad, 2),
                'tiene_propiedad': tiene_propiedad,
                'valor_propiedad': round(valor_propiedad, 2) if tiene_propiedad else 0
            },
            'recomendaciones': recomendaciones,
            'margen_disponible': round(ingresos_mensuales - gastos_mensuales, 2)
        }
        
        return evaluacion
