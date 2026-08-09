"""
Credenziali IBM Quantum (OPZIONALE).

1. Copia questo file come qiskit_secrets.local.py (stessa cartella).
2. Inserisci il token ottenuto da https://quantum.ibm.com/
3. qiskit_secrets.local.py e' gia' nel .gitignore: non verra' committato.

Il notebook funziona interamente con il simulatore locale Aer anche senza token.
Per eseguire su hardware IBM serve inoltre: pip install qiskit-ibm-runtime
"""

IBM_TOKEN = "Rm-ThBgA-OTLbHU2S9Z2vqLZoARrX3gTv0lJO8fIY1Zx"  # es. "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
IBM_CHANNEL = "ibm_quantum"  # o "ibm_cloud" se usi IBM Cloud
IBM_INSTANCE = "crn:v1:bluemix:public:quantum-computing:us-east:a/e3bc651acc4b4649b72fe11106e46341:32e9dcfc-0249-46eb-af3f-0ddf008bd7b1::"  # opzionale: es. "ibm-q/open/main" o il tuo CRN


