## Task ocr: n=300, gold distribution {'legitimate': 274, 'ocr_error': 26}
- ocr_sonnet: accuracy 93.0% on 300 | legitimate recall 96%, ocr_error recall 65%
- ocr_haiku: accuracy 89.2% on 297 | legitimate recall 92%, ocr_error recall 65%
- ocr_jev: accuracy 86.7% on 300; conf≥0.5: 93.8% on 211 (70% coverage); conf≥0.7: 95.6% on 158 (53% coverage); conf≥0.85: 97.0% on 99 (33% coverage) | legitimate recall 91%, ocr_error recall 46%
## Task seg: n=196, gold distribution {'article': 103, 'subarticle': 80, 'reject': 13}
- seg_opus: accuracy 99.5% on 196 | article recall 100%, reject recall 92%, subarticle recall 100%
- seg_sonnet: accuracy 76.0% on 196 | article recall 100%, reject recall 77%, subarticle recall 45%
- seg_haiku: accuracy 92.3% on 196 | article recall 90%, reject recall 85%, subarticle recall 96%
- seg_jev: accuracy 61.7% on 196; conf≥0.5: 62.4% on 170 (87% coverage); conf≥0.7: 67.2% on 134 (68% coverage); conf≥0.85: 64.6% on 82 (42% coverage) | article recall 99%, reject recall 77%, subarticle recall 11%