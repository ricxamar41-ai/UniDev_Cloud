#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo: ui.py
Interfaz Gradio para RACHEL MASTER
"""

import gradio as gr
import subprocess
import re
import logging

# Logger con fallback
try:
    from logger import log_info, log_error
except ImportError:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    log_info = logging.info
    log_error = logging.error

# Importar brain
try:
    from brain import procesar_cerebro
except ImportError as e:
    log_error(f"Error importando brain: {e}")
    procesar_cerebro = None

def rachel_engine(mensaje: str, historial: list):
    """Motor principal de RACHEL MASTER"""
    if not mensaje:
        return ""
    
    # MANDO ROOT (Solo con clave RICARDO2026)
    if "RICARDO2026" in mensaje.upper():
        try:
            from monitor import auditar_recursos_maestros
            
            rep = auditar_recursos_maestros("RICARDO2026")
            comando = mensaje.upper().replace("RICARDO2026", "").strip()
            
            if not comando:
                return f"🛡️ NÚCLEO: RAM {rep.get('ram', 'N/A')}% | CPU {rep.get('cpu', 'N/A')}%"
            
            # Ejecutar comando de forma segura
            resultado = subprocess.run(
                comando, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if resultado.returncode != 0:
                return f"❌ ERROR: {resultado.stderr}"
            
            return f"🛡️ REPORTE (RAM: {rep.get('ram', 'N/A')}%):\n\n{resultado.stdout}"
            
        except subprocess.TimeoutExpired:
            return "❌ ERROR: Comando demasiado lento"
        except ImportError:
            return "❌ ERROR: Módulo 'monitor' no encontrado"
        except Exception as e:
            return f"❌ ERROR: {str(e)}"
    
    # CHARLA NORMAL (Procesamiento con IA)
    try:
        if procesar_cerebro is None:
            return "❌ Error: Módulo brain no disponible"
        
        respuesta = procesar_cerebro(mensaje, historial)
        res_str = str(respuesta)
        
        # Normalizar nombre
        res_str = re.sub(r'rachel\s*master', 'RACHEL MASTER', res_str, flags=re.IGNORECASE)
        
        return res_str
        
    except Exception as e:
        return f"❌ Error en procesamiento: {str(e)}"

# INTERFAZ GRADIO
with gr.Blocks(title="RACHEL MASTER") as interfaz:
    gr.Markdown("# 👑 **RACHEL MASTER** 👑\n### IA Autónoma de Ricardo Pino Peña")
    
    gr.ChatInterface(
        fn=rachel_engine,
        title="RACHEL MASTER",
        description="Asistente IA de Nivel 3"
    )

if __name__ == "__main__":
    interfaz.launch(
        server_name="0.0.0.0", 
        server_port=7860, 
        theme=gr.themes.Soft()
    )
