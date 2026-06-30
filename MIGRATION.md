# Aletheus™ Genesis 0.3 Runtime Core Migration

1. Backup:
```bash
cp -R . ../AletheusOS_Pre_Genesis_03_Backup
```

2. Merge into project root:
```bash
cp -R Aletheus_Sprint_A3_Runtime_Core/* .
```

3. Test:
```bash
PYTHONPATH=. python tests/test_aletheus_runtime_a3.py
```

4. Launch:
```bash
PYTHONPATH=. streamlit run ui/pages/aletheus_runtime_console.py
```
