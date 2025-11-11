# test_evaluacion.py
# Script de prueba para el módulo de evaluación crediticia

from evaluacion_credito import EvaluadorCredito
import json

def prueba_evaluacion():
    """Prueba el módulo de evaluación crediticia"""
    
    evaluador = EvaluadorCredito()
    
    print("\n" + "="*60)
    print("🤖 PRUEBA DEL SISTEMA DE EVALUACIÓN CREDITICIA")
    print("="*60)
    
    # Test 1: Cliente Apto
    print("\n📊 Test 1: Cliente Apto para Préstamo")
    print("-" * 60)
    eval1 = evaluador.evaluar_cliente(
        sueldo=3500,
        otros_ingresos=500,
        gastos_vivienda=800,
        otras_deudas=200,
        estado_actual='al_dia'
    )
    print(f"Puntuación: {eval1['puntuacion_final']}/100")
    print(f"Apto: {eval1['apto_prestamo']}")
    print(f"Riesgo: {eval1['nivel_riesgo']}")
    print(f"Ingresos: ${eval1['detalle']['ingresos_mensuales']}")
    print(f"Gastos: ${eval1['detalle']['gastos_mensuales']}")
    print(f"Margen: ${eval1['margen_disponible']}")
    print(f"Ratio: {eval1['detalle']['ratio_deuda']}%")
    
    # Test 2: Cliente Condicionado
    print("\n📊 Test 2: Cliente Condicionado")
    print("-" * 60)
    eval2 = evaluador.evaluar_cliente(
        sueldo=2000,
        otros_ingresos=300,
        gastos_vivienda=600,
        otras_deudas=400,
        estado_actual='retraso_leve'
    )
    print(f"Puntuación: {eval2['puntuacion_final']}/100")
    print(f"Apto: {eval2['apto_prestamo']}")
    print(f"Riesgo: {eval2['nivel_riesgo']}")
    print(f"Ingresos: ${eval2['detalle']['ingresos_mensuales']}")
    print(f"Gastos: ${eval2['detalle']['gastos_mensuales']}")
    print(f"Margen: ${eval2['margen_disponible']}")
    print(f"Ratio: {eval2['detalle']['ratio_deuda']}%")
    
    # Test 3: Cliente No Apto
    print("\n📊 Test 3: Cliente NO Apto para Préstamo")
    print("-" * 60)
    eval3 = evaluador.evaluar_cliente(
        sueldo=1500,
        otros_ingresos=0,
        gastos_vivienda=900,
        otras_deudas=600,
        estado_actual='impago'
    )
    print(f"Puntuación: {eval3['puntuacion_final']}/100")
    print(f"Apto: {eval3['apto_prestamo']}")
    print(f"Riesgo: {eval3['nivel_riesgo']}")
    print(f"Ingresos: ${eval3['detalle']['ingresos_mensuales']}")
    print(f"Gastos: ${eval3['detalle']['gastos_mensuales']}")
    print(f"Margen: ${eval3['margen_disponible']}")
    print(f"Ratio: {eval3['detalle']['ratio_deuda']}%")
    
    # Mostrar estructura de evaluación
    print("\n📋 Estructura Completa de Evaluación (Test 1):")
    print("-" * 60)
    print(json.dumps(eval1, indent=2, ensure_ascii=False))
    
    print("\n" + "="*60)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("="*60 + "\n")

if __name__ == '__main__':
    prueba_evaluacion()
