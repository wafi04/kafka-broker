import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from typing import Dict, Any
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataAnalyzer:
    def __init__(self, file: str):
        """
        Inisialisasi DataAnalyzer dengan file CSV
        """
        self.file = file
        self.df = None
        self.info = {}
        
    def load_data(self) -> None:
        """
        Membaca file CSV dan menyimpannya dalam DataFrame
        """
        try:
            logger.info(f"Membaca file: {self.file}")
            self.df = pd.read_csv(self.file)
        except Exception as e:
            logger.error(f"Error membaca file: {str(e)}")
            raise

    def analyze_data(self) -> Dict[str, Any]:
        """
        Menganalisis data dan menghasilkan statistik
        """
        if self.df is None:
            self.load_data()

        try:
            self.info = {
                'jumlah_baris': len(self.df),
                'jumlah_kolom': len(self.df.columns),
                'nama_kolom': list(self.df.columns),
                'tipe_data': self.df.dtypes.to_dict(),
                'info_numerik': {},
                'missing_values': self.df.isnull().sum().to_dict(),
                'correlation_matrix': None
            }

            kolom_numerik = self.df.select_dtypes(include=['int64', 'float64']).columns
            for kolom in kolom_numerik:
                data = self.df[kolom].values
                self.info['info_numerik'][kolom] = {
                    'mean': np.mean(data),
                    'median': np.median(data),
                    'modus': float(self.df[kolom].mode().iloc[0]),
                    'range': np.ptp(data),
                    'min': np.min(data),
                    'max': np.max(data),
                    'variance': np.var(data),
                    'standar_deviasi': np.std(data),
                    'skewness': float(self.df[kolom].skew()),
                    'kurtosis': float(self.df[kolom].kurtosis()),
                    'quartiles': np.percentile(data, [25, 50, 75]),
                    'iqr': np.percentile(data, 75) - np.percentile(data, 25)
                }

            if len(kolom_numerik) > 1:
                self.info['correlation_matrix'] = self.df[kolom_numerik].corr()

            return self.info

        except Exception as e:
            logger.error(f"Error dalam analisis: {str(e)}")
            raise

    def plot_visualizations(self, output_dir: str = './plots') -> None:
        """
        Membuat visualisasi data menggunakan matplotlib dan seaborn
        """
        try:
            # Buat direktori jika belum ada
            os.makedirs(output_dir, exist_ok=True)
            
            # Menggunakan style default matplotlib yang valid
            plt.style.use('default')
            
            # Set tema seaborn
            sns.set_theme(style="whitegrid")
            
            kolom_numerik = self.df.select_dtypes(include=['int64', 'float64']).columns

            # 1. Distribution plots
            for kolom in kolom_numerik:
                plt.figure(figsize=(10, 6))
                sns.histplot(data=self.df[kolom], kde=True)
                plt.title(f'Distribusi {kolom}')
                plt.xlabel(kolom)
                plt.ylabel('Frekuensi')
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, f'distribusi_{kolom}.png'))
                plt.close()

            # 2. Box plots
            if len(kolom_numerik) > 0:
                plt.figure(figsize=(12, 6))
                sns.boxplot(data=self.df[kolom_numerik])
                plt.title('Box Plot Kolom Numerik')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, 'boxplot_all.png'))
                plt.close()

            # 3. Correlation heatmap
            if len(kolom_numerik) > 1:
                plt.figure(figsize=(10, 8))
                correlation_matrix = self.df[kolom_numerik].corr()
                sns.heatmap(correlation_matrix, 
                           annot=True, 
                           cmap='coolwarm', 
                           center=0,
                           fmt='.2f')
                plt.title('Correlation Heatmap')
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, 'correlation_heatmap.png'))
                plt.close()

            # 4. Missing values plot
            plt.figure(figsize=(12, 6))
            missing_data = self.df.isnull().sum()
            sns.barplot(x=missing_data.index, y=missing_data.values)
            plt.title('Missing Values per Column')
            plt.xlabel('Columns')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'missing_values.png'))
            plt.close()

            # 5. Pair plot untuk kolom numerik (jika tidak terlalu banyak kolom)
            if 2 <= len(kolom_numerik) <= 5:
                sns.pairplot(self.df[kolom_numerik])
                plt.savefig(os.path.join(output_dir, 'pair_plot.png'))
                plt.close()

            logger.info(f"Visualisasi berhasil disimpan di direktori: {output_dir}")

        except Exception as e:
            logger.error(f"Error dalam pembuatan visualisasi: {str(e)}")
            raise

def tampilkan_hasil(hasil: Dict[str, Any]) -> None:
    """
    Menampilkan hasil analisis dalam format yang mudah dibaca.
    """
    try:
        print("\n=== INFORMASI DATASET ===")
        print(f"Jumlah baris: {hasil['jumlah_baris']:,}")
        print(f"Jumlah kolom: {hasil['jumlah_kolom']}")
        
        print("\n=== NAMA DAN TIPE KOLOM ===")
        for kolom in hasil['nama_kolom']:
            print(f"- {kolom:<20} (Tipe: {hasil['tipe_data'][kolom]})")
        
        print("\n=== MISSING VALUES ===")
        missing_found = False
        for kolom, jumlah in hasil['missing_values'].items():
            if jumlah > 0:
                missing_found = True
                print(f"- {kolom:<20}: {jumlah:,} nilai hilang")
        if not missing_found:
            print("Tidak ada nilai yang hilang dalam dataset")
        
        print("\n=== STATISTIK KOLOM NUMERIK ===")
        for kolom, stats in hasil['info_numerik'].items():
            print(f"\n{kolom.upper()}:")
            print(f"- Rata-rata       : {stats['mean']:,.2f}")
            print(f"- Median         : {stats['median']:,.2f}")
            print(f"- Modus          : {stats['modus']:,.2f}")
            print(f"- Range          : {stats['range']:,.2f}")
            print(f"- Minimum        : {stats['min']:,.2f}")
            print(f"- Maximum        : {stats['max']:,.2f}")
            print(f"- Variance       : {stats['variance']:,.2f}")
            print(f"- Std. Deviasi   : {stats['standar_deviasi']:,.2f}")
            print(f"- Skewness       : {stats['skewness']:,.2f}")
            print(f"- Kurtosis       : {stats['kurtosis']:,.2f}")
        
    except Exception as e:
        logger.error(f"Error dalam menampilkan hasil: {str(e)}")
        raise
