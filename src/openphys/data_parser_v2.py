import pandas as pd
import numpy as np
from typing import Dict, Any

class ScientificDataParser:
    def __init__(self):
        pass

    def parse_api_response(self, raw_data: Dict[str, Any], target_fields: list) -> Dict[str, np.ndarray]:
        """
        API'den dönen JSON veya CSV verilerini ayıklar.
        Veri bilimi ardışık düzenlerinde (pipeline) kullanılan yapıya uygun olarak, 
        ham veriyi pandas DataFrame üzerinden filtreleyip makine öğrenmesi modeline (PINN) hazırlar.
        """
        # API'den gelen mock veri yapısını pandas DataFrame'e çeviriyoruz
        if "results" in raw_data:
            df = pd.DataFrame(raw_data["results"])
        else:
            # Yedek boş yapı
            df = pd.DataFrame(columns=["x", "y"] + target_fields)

        # Eksik veya bozuk satırları temizle
        df = df.dropna()

        # Koordinatları (x, y, z) ayır
        coord_cols = [col for col in ["x", "y", "z"] if col in df.columns]
        coords_array = df[coord_cols].values.astype(np.float32)

        # Hedef fiziksel alanları (örn: hız, basınç, sıcaklık) ayır
        targets = {}
        for field in target_fields:
            if field in df.columns:
                targets[field] = df[field].values.astype(np.float32).reshape(-1, 1)

        return {
            "coords": coords_array,
            "targets": targets
        }