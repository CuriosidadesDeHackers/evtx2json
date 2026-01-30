
## 📌 Descripción general

Este repositorio contiene **3 scripts** que permiten convertir archivos `.evtx` (logs de eventos de Windows) a formato **JSON**, facilitando su análisis con herramientas como:

- jq
- Elasticsearch / OpenSearch
- Splunk
- Scripts de análisis propios
- Machine Learning / detección

Los scripts manejan correctamente:
- Namespaces XML
- Eventos repetidos
- Conversión XML → dict → JSON

---

## 📂 Scripts incluidos

### 1️⃣ `evtx_to_json.py`

Convierte **un solo archivo `.evtx`** en un archivo JSON.

**Características**
- Entrada: un archivo `.evtx`
- Salida: lista JSON con todos los eventos
- Cada evento es un diccionario limpio (sin nombre de archivo)

**Uso**
```bash
python evtx_to_json.py Security.evtx output.json
````

**Salida**

```json
[
  {
    "Event": {
      "System": {...},
      "EventData": {...}
    }
  }
]
```

---

### 2️⃣ `evtx_folder_to_json.py`

Convierte **todos los `.evtx` de una carpeta** en **un único JSON**.

**Características**

* Procesa múltiples archivos `.evtx`
* Incluye el nombre del archivo original (`_evtx_file`)
* Salida en forma de **lista JSON**
* Ideal para saber de qué log proviene cada evento

**Uso**

```bash
python evtx_folder_to_json.py ./logs output.json
```

**Salida**

```json
[
  {
    "_evtx_file": "Security.evtx",
    "Event": {...}
  },
  {
    "_evtx_file": "System.evtx",
    "Event": {...}
  }
]
```

---

### 3️⃣ `2evtx_folder_to_json.py`

Versión alternativa que convierte **una carpeta completa de `.evtx`** a JSON, pero usando un **formato indexado**.

**Características**

* Cada evento tiene una clave única (`Event_000001`, `Event_000002`, etc.)
* **NO** incluye el nombre del archivo `.evtx`
* Útil para ingestión directa en bases de datos o pipelines

**Uso**

```bash
python 2evtx_folder_to_json.py ./logs output.json
```

**Salida**

```json
{
  "Event_000001": {
    "Event": {...}
  },
  "Event_000002": {
    "Event": {...}
  }
}
```

---

## 🧰 Requisitos

Instala las dependencias necesarias:

```bash
pip install python-evtx lxml
```

Python recomendado: **3.8+**

---

## 🎯 Casos de uso

* Análisis forense de sistemas Windows
* Threat hunting
* Normalización de logs
* Ingesta en SIEM
* Automatización de detecciones
* Procesamiento masivo de eventos

---

## ⚠️ Notas

* Los scripts **no modifican** los archivos originales
* Los eventos corruptos se ignoran mostrando error por pantalla
* Diseñado para entornos de análisis, no producción en tiempo real

---

## 🤘 Autor

Creado por **CuriosidadesDeHackers**

Si te sirve, ⭐ el repo y compártelo.


